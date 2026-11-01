#!/usr/bin/env python3
"""Run the Ask Tianjie eval set against a deployment (or `wrangler pages dev`).

  python3 tools/ask_eval.py --base http://localhost:8788
  python3 tools/ask_eval.py --base https://tianjie.me --invite "$EVAL_INVITE" --out /tmp/ask-eval.json

Each question in ask/evals/questions.jsonl says what should happen:
  answer     cited answer (ALL_CITED, or PARTIAL as a warning) that cites one of must_cite
  no_source  the assistant declines (NO_SOURCE; UNCITED = blocked, also counts as declined)
  handoff    routed to Tianjie (HANDOFF) without calling the model
  any        anything but ERROR
In demo mode (no model key) only routing and retrieval are checked: the top-5
retrieval preview must contain one of must_cite.

Production has a small anonymous quota, so pass an invite token with a high quota:
  python3 tools/ask_invite.py --label eval --quota 300 --days 1
"""
import argparse, json, os, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ask(base, q, invite):
    req = urllib.request.Request(f"{base.rstrip('/')}/api/ask", method='POST',
                                 data=json.dumps({'q': q, 'invite': invite}).encode(),
                                 headers={'content-type': 'application/json'})
    events, t0 = {}, time.time()
    try:
        with urllib.request.urlopen(req, timeout=90) as res:
            event, data = 'message', []
            for raw in res:
                line = raw.decode('utf-8').rstrip('\n')
                if line.startswith('event:'):
                    event = line[6:].strip()
                elif line.startswith('data:'):
                    data.append(line[5:].strip())
                elif line == '':
                    if data:
                        try:
                            events.setdefault(event, []).append(json.loads('\n'.join(data)))
                        except json.JSONDecodeError:
                            pass
                    event, data = 'message', []
    except urllib.error.HTTPError as e:
        return {'http_error': e.code, 'body': e.read().decode()[:200]}, time.time() - t0
    return events, time.time() - t0


def judge(item, ev):
    if 'http_error' in ev:
        return 'FAIL', f"HTTP {ev['http_error']} {ev['body']}"
    done = (ev.get('done') or [{}])[-1]
    r = done.get('receipt') or {}
    v = r.get('verdict')
    meta = (ev.get('meta') or [{}])[0]
    demo = meta.get('demo')
    exp = item['expect']
    answer = done.get('answer', '')
    if v == 'ERROR':
        return 'FAIL', f"ERROR {r.get('error', '')}"
    if 'http://' in answer or 'https://' in answer:
        return 'FAIL', 'URL in answer'
    if exp == 'handoff':
        return ('PASS', 'handoff') if v == 'HANDOFF' else ('FAIL', f'expected HANDOFF, got {v}')
    if v == 'HANDOFF':
        return 'FAIL', f"routed to handoff ({r.get('topic')})"
    cands = [c['id'] for c in (ev.get('candidates') or [[]])[0]]
    hit = lambda ids: any(i.startswith(p) for i in ids for p in item['must_cite'])
    if demo:
        if exp == 'answer' and item['must_cite']:
            return ('PASS', 'demo: retrieval ok') if hit(cands) else ('WARN', f'demo: retrieval missed; top-5 {cands}')
        return 'SKIP', 'demo mode: model behaviour not tested'
    if exp == 'any':
        return 'PASS', v
    if exp == 'no_source':
        return ('PASS', v) if v in ('NO_SOURCE', 'UNCITED') else ('FAIL', f'expected decline, got {v}: {answer[:80]}')
    # answer
    if v not in ('ALL_CITED', 'PARTIAL'):
        return 'FAIL', f'expected cited answer, got {v}: {answer[:80]}'
    if item['must_cite'] and not hit(r.get('cited') or []):
        return 'WARN', f"cited {r.get('cited')} but none of {item['must_cite']}"
    return ('PASS', v) if v == 'ALL_CITED' else ('WARN', 'PARTIAL: some paragraphs uncited')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://localhost:8788')
    ap.add_argument('--invite', default=os.environ.get('EVAL_INVITE', ''))
    ap.add_argument('--only', default='', help='comma-separated question ids')
    ap.add_argument('--out', default='')
    a = ap.parse_args()
    items = [json.loads(l) for l in open(os.path.join(ROOT, 'ask', 'evals', 'questions.jsonl'), encoding='utf-8') if l.strip()]
    if a.only:
        keep = set(a.only.split(','))
        items = [i for i in items if i['id'] in keep]
    rows, tally, cost, lat = [], {}, 0.0, []
    for it in items:
        ev, dt = ask(a.base, it['q'], a.invite)
        status, note = judge(it, ev)
        tally[status] = tally.get(status, 0) + 1
        r = ((ev.get('done') or [{}])[-1].get('receipt') or {}) if isinstance(ev, dict) else {}
        if isinstance(r.get('cost_usd'), (int, float)):
            cost += r['cost_usd']
        if r.get('ttfb_ms') is not None:
            lat.append(r['ttfb_ms'])
        rows.append({'id': it['id'], 'expect': it['expect'], 'status': status, 'verdict': r.get('verdict'), 'note': note,
                     'cited': r.get('cited'), 'ttfb_ms': r.get('ttfb_ms'), 'total_ms': r.get('total_ms'), 'seconds': round(dt, 2)})
        print(f"{status:<5} {it['id']:<12} {it['expect']:<9} {str(r.get('verdict')):<10} {note}")
    print('\n' + '  '.join(f'{k} {v}' for k, v in sorted(tally.items())) +
          (f'  · est. cost ${cost:.4f}' if cost else '') + (f'  · median first token {sorted(lat)[len(lat) // 2]} ms' if lat else ''))
    if a.out:
        json.dump({'base': a.base, 'at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'tally': tally, 'rows': rows}, open(a.out, 'w'), ensure_ascii=False, indent=2)
    sys.exit(1 if tally.get('FAIL') else 0)


if __name__ == '__main__':
    main()
