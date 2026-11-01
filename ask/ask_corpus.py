"""Ask Tianjie · corpus builder (called from build.py, standard library only).

Writes
  public/ask/index.json        every public source the assistant may cite, chunked,
                               with BM25 term stats (the "open context" for the agent)
  public/ask/index.html        the /ask/ page (from hub/ask.html)
  public/ask/cards/index.html  published judgment cards (from ask/cards/*.md)
and appends /ask/ to sitemap.xml and llms.txt.

Only material that is already public on tianjie.me goes in. Draft cards
(status: draft) are skipped. tokenize() must match ask/lib/text.js.
"""
import hashlib
import html
import json
import os
import re
from html.parser import HTMLParser

TOKEN_RE = re.compile(r'[a-z0-9]+(?:[.\-_][a-z0-9]+)*|[㐀-鿿豈-﫿]+')
CJK_RE = re.compile(r'^[㐀-鿿豈-﫿]+$')
STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'can', 'do', 'does', 'did', 'for', 'from',
    'has', 'have', 'he', 'his', 'him', 'how', 'i', 'in', 'is', 'it', 'its', 'me', 'my', 'of',
    'on', 'or', 'she', 'so', 'that', 'the', 'their', 'there', 'this', 'to', 'was', 'what',
    'when', 'where', 'which', 'who', 'why', 'will', 'with', 'you', 'your', 'about', 'tell',
}
MAX_CHUNK = 1400


def tokenize(text):
    out = []
    for m in TOKEN_RE.finditer(str(text or '').lower()):
        s = m.group(0)
        if CJK_RE.match(s):
            if len(s) == 1:
                out.append(s)
            else:
                out.extend(s[i:i + 2] for i in range(len(s) - 1))
        elif (len(s) > 1 and s not in STOPWORDS) or s.isdigit():
            out.append(s)
    return out


def estimate_tokens(text):
    s = str(text or '')
    cjk = len(re.findall(r'[㐀-鿿豈-﫿]', s))
    words = len(re.sub(r'[㐀-鿿豈-﫿]', ' ', s).split())
    return int(cjk * 1.1 + words * 1.4) + 1


class _Text(HTMLParser):
    BLOCK = {'p', 'li', 'h1', 'h2', 'h3', 'h4', 'div', 'section', 'br', 'dt', 'dd', 'tr', 'pre', 'ul', 'ol', 'details', 'summary'}

    def __init__(self):
        super().__init__()
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript', 'svg'):
            self.skip += 1
        elif tag in self.BLOCK:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript', 'svg'):
            self.skip = max(0, self.skip - 1)
        elif tag in self.BLOCK:
            self.parts.append('\n')
        elif tag in ('i', 'b', 'span', 'a', 'code', 'strong', 'em', 'small', 'sup'):
            self.parts.append(' ')

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def html_to_text(s):
    p = _Text()
    p.feed(s)
    lines = [re.sub(r'[ \t ]+', ' ', ln).strip() for ln in ''.join(p.parts).split('\n')]
    out, blank = [], False
    for ln in lines:
        if ln:
            out.append(ln)
            blank = False
        elif not blank and out:
            out.append('')
            blank = True
    return '\n'.join(out).strip()


def split_text(text, limit=MAX_CHUNK):
    paras = [p for p in re.split(r'\n\s*\n|\n', text) if p.strip()]
    parts, cur = [], ''
    for p in paras:
        if cur and len(cur) + len(p) + 1 > limit:
            parts.append(cur)
            cur = p
        else:
            cur = f'{cur}\n{p}' if cur else p
    if cur:
        parts.append(cur)
    return parts or ['']


def parse_card(path):
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', raw, re.S)
    meta, body = {}, raw
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip().strip('"')
        body = m.group(2)
    body = re.sub(r'<!--.*?-->', '', body, flags=re.S).strip()
    meta.setdefault('id', os.path.splitext(os.path.basename(path))[0])
    meta['body'] = body
    return meta


def card_text(body):
    return re.sub(r'^#+\s*', '', body, flags=re.M).strip()


def card_html(body, esc):
    out, para, items, kind = [], [], [], None

    def flush():
        nonlocal para, items, kind
        if para:
            out.append(f'<p>{esc(" ".join(para))}</p>')
            para = []
        if items:
            out.append(f'<{kind}>' + ''.join(f'<li>{esc(i)}</li>' for i in items) + f'</{kind}>')
            items, kind = [], None

    for line in body.splitlines():
        s = line.strip()
        if not s:
            flush()
        elif s.startswith('#'):
            flush()
            out.append(f'<h3>{esc(s.lstrip("#").strip())}</h3>')
        elif re.match(r'^(\d+\.|-)\s+', s):
            if para:
                flush()
            k = 'ol' if s[0].isdigit() else 'ul'
            if kind and kind != k:
                flush()
            kind = k
            items.append(re.sub(r'^(\d+\.|-)\s+', '', s))
        else:
            if items:
                flush()
            para.append(s)
    flush()
    return '\n'.join(out)


def build_ask(root, out, hub, base, site, person, themes, latest, esc, today, extras=None):
    chunks = []

    def add(cid, title, url, text, date=None, kind='page'):
        text = str(text or '').strip()
        if not text:
            return
        parts = split_text(text)
        for i, part in enumerate(parts):
            pid = cid if len(parts) == 1 else f'{cid}-{i + 1}'
            ptitle = title if len(parts) == 1 else f'{title} ({i + 1}/{len(parts)})'
            chunks.append({'id': pid, 'title': ptitle, 'url': url, 'date': date, 'kind': kind, 'text': part})

    # about (person.json): the facts Tianjie confirms
    if person:
        add('about#intro', 'About · Tianjie Sun', '/about/',
            '\n'.join(filter(None, [
                f"{person['name']}（{person.get('name_zh', '')}，{person.get('alias', '')}），{person.get('location', '')}",
                person.get('persona'), person.get('lede'), person.get('persona_zh'), person.get('lede_zh')])), kind='about')
        now_zh = person.get('now_zh') or []
        add('about#now', 'About · Now', '/about/#now',
            '\n'.join(f'- {en}' + (f'（{now_zh[i]}）' if i < len(now_zh) else '') for i, en in enumerate(person.get('now', []))), date=today, kind='about')
        add('about#facts', 'About · Facts', '/about/#facts',
            '\n'.join(f"- {f['k']}: {f['v']}" for f in person.get('facts', [])), kind='about')
        add('about#evidence', 'About · Things you can open', '/about/#evidence',
            '\n'.join(f"- {e['title']}: {e['desc']}" for e in person.get('evidence', [])), kind='about')
        links = []
        for l in person.get('links', []):
            u = l['url']
            if 'github.com/' in u:
                links.append(f"- {l['label']}: {u.split('://', 1)[-1]}")
            else:
                links.append(f"- {l['label']}")
        add('about#contact', 'About · Contact', '/about/#contact',
            '\n'.join(links + [person.get('contact_note', ''), person.get('contact_note_zh', ''),
                               'On tianjie.me/ask/ visitors can also leave an email for Tianjie to reply personally.']), kind='about')

    # the site itself
    projects = '\n'.join(f"- {p['title']}：{p['desc']}" for p in site.get('projects', []))
    add('site', f"{site['name']} · 网站首页", '/',
        f"{site['name']}：{site['tagline']}\n{html_to_text(site.get('about', ''))}\n长期专题：\n{projects}", kind='site')

    # /how/ (built page)
    how_path = os.path.join(out, 'how', 'index.html')
    if os.path.exists(how_path):
        page = open(how_path, encoding='utf-8').read()
        hero = re.search(r'<section class="hero">(.*?)</section>', page, re.S)
        if hero:
            add('how#intro', '制作说明 · 这些题是怎么做出来的', '/how/', html_to_text(hero.group(1)), kind='how')
        for sid, inner in re.findall(r'<section class="sec" id="([\w-]+)">(.*?)</section>', page, re.S):
            h = re.search(r'<h2>(.*?)</h2>', inner, re.S)
            head = html_to_text(h.group(1)) if h else sid
            add(f'how#{sid}', f'制作说明 · {head}', f'/how/#{sid}', html_to_text(inner), kind='how')

    # 一周一题 themes (metadata only in v0)
    for m in reversed(themes):
        srcs = '；'.join(str(s)[:160] for s in (m.get('sources') or [])[:2])
        add(f"t/{m['slug']}", f"一周一题 第 {m['no']} 题 · {m['title']}", m['url'],
            '\n'.join(filter(None, [
                f"一周一题 · 第 {m['no']} 题 · {m['date']}", m['title'], m.get('subtitle'), m.get('summary'),
                f"形式：{m['format']}" if m.get('format') else '',
                f"标签：{'、'.join(m.get('tags') or [])}" if m.get('tags') else '',
                f"阅读时间：{m['reading_time']}" if m.get('reading_time') else '',
                f"主要出处：{srcs}" if srcs else ''])), date=m['date'], kind='theme')

    # 号外 extras: specials outside the weekly series, /x/<slug>/ (metadata only, like themes)
    for m in reversed(extras or []):
        add(f"x/{m['slug']}", f"号外 · {m['title']}", m['url'],
            '\n'.join(filter(None, [
                f"号外（周更之外的专题，不占题号）· {m['date']}", m['title'], m.get('subtitle'), m.get('summary'),
                f"形式：{m['format']}" if m.get('format') else '',
                f"标签：{'、'.join(m.get('tags') or [])}" if m.get('tags') else '',
                f"阅读时间：{m['reading_time']}" if m.get('reading_time') else ''])), date=m['date'], kind='extra')

    # 合读 podcast
    pod = site.get('podcast')
    pod_dir = os.path.join(root, 'podcast', 'episodes')
    if pod and os.path.isdir(pod_dir):
        pbase = pod.get('path', '/listen/')
        add('listen', f"{pod['name']} · 播客", pbase, f"{pod['name']}：{pod['tagline']}\n{html_to_text(pod.get('about', ''))}", kind='podcast')
        for d in sorted(os.listdir(pod_dir)):
            p = os.path.join(pod_dir, d)
            mp = os.path.join(p, 'meta.json')
            if not re.match(r'^\d{4}-\d{2}-\d{2}-[a-z0-9-]+$', d) or not os.path.exists(mp):
                continue
            e = json.load(open(mp, encoding='utf-8'))
            if e.get('draft'):
                continue
            slug, date = e.get('slug', d[11:]), e.get('date', d[:10])
            notes_p = os.path.join(p, 'notes.html')
            notes = html_to_text(open(notes_p, encoding='utf-8').read()) if os.path.exists(notes_p) else ''
            add(f'listen/{slug}', f"{pod['name']} · {e['title']}", f'{pbase}{slug}/',
                '\n'.join(filter(None, [e['title'], e.get('subtitle'), e.get('summary'),
                                        ('书目：' + '、'.join(e.get('books', []))) if e.get('books') else '', notes])), date=date, kind='podcast')

    # judgment cards
    cards = []
    cdir = os.path.join(root, 'ask', 'cards')
    for f in sorted(os.listdir(cdir)) if os.path.isdir(cdir) else []:
        if f.endswith('.md'):
            c = parse_card(os.path.join(cdir, f))
            if c.get('status') == 'published':
                cards.append(c)
                add(f"card/{c['id']}", f"判断卡 · {c.get('title_zh') or c['id']} / {c.get('title_en', '')}",
                    f"/ask/cards/#{c['id']}", card_text(c['body']), date=c.get('updated'), kind='card')

    # English keywords for Chinese-only sources (ask/aliases.json, or keywords_en in a theme's meta.json)
    alias_path = os.path.join(root, 'ask', 'aliases.json')
    aliases = json.load(open(alias_path, encoding='utf-8')) if os.path.exists(alias_path) else {}
    for m in themes:
        if m.get('keywords_en'):
            aliases[f"t/{m['slug']}"] = m['keywords_en']
    for m in extras or []:
        if m.get('keywords_en'):
            aliases[f"x/{m['slug']}"] = m['keywords_en']
    for c in chunks:
        base_id = re.sub(r'-\d+$', '', c['id'])
        if base_id in aliases:
            c['text'] = f"{c['text']}\nKeywords (EN): {aliases[base_id]}"

    # BM25 stats
    df = {}
    total = 0
    for c in chunks:
        toks = tokenize(f"{c['title']}\n{c['text']}")
        tf = {}
        for t in toks:
            tf[t] = tf.get(t, 0) + 1
        c['tf'], c['len'] = tf, len(toks)
        total += len(toks)
        for t in tf:
            df[t] = df.get(t, 0) + 1
    est = sum(estimate_tokens(c['title'] + '\n' + c['text']) for c in chunks)
    version = hashlib.sha1(json.dumps([[c['id'], c['text']] for c in chunks], ensure_ascii=False).encode()).hexdigest()[:10]
    index = {
        'version': version, 'built': today, 'n': len(chunks), 'avgdl': (total / len(chunks)) if chunks else 1,
        'est_tokens': est, 'core': [c['id'] for c in chunks if c['id'] in ('about#intro', 'about#facts', 'card/what-the-assistant-wont-answer')],
        'df': df, 'chunks': chunks,
    }
    os.makedirs(os.path.join(out, 'ask', 'cards'), exist_ok=True)
    with open(os.path.join(out, 'ask', 'index.json'), 'w', encoding='utf-8') as fh:
        json.dump(index, fh, ensure_ascii=False, separators=(',', ':'))

    # pages
    og = f"{base}{latest['url']}cover.png" if latest and latest.get('has_cover') else ''
    year = today[:4]
    ts_key = os.environ.get('TURNSTILE_SITE_KEY', '').strip()
    tpl = open(os.path.join(hub, 'ask.html'), encoding='utf-8').read()
    page = (tpl.replace('{{SITE_NAME}}', esc(site['name'])).replace('{{BASE}}', base).replace('{{YEAR}}', year)
            .replace('{{OG_IMAGE}}', og).replace('{{CORPUS_VERSION}}', version).replace('{{CHUNKS}}', str(len(chunks)))
            .replace('{{TURNSTILE_SITE_KEY}}', esc(ts_key))
            .replace('{{TURNSTILE_SCRIPT}}', '<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>' if ts_key else ''))
    with open(os.path.join(out, 'ask', 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(page)

    ctpl = open(os.path.join(hub, 'ask_cards.html'), encoding='utf-8').read()
    cards_html = ''.join(
        f'<article class="card" id="{esc(c["id"])}"><div class="kicker">判断卡 · {esc(c.get("updated", ""))}</div>'
        f'<h2>{esc(c.get("title_zh", c["id"]))}<small>{esc(c.get("title_en", ""))}</small></h2>'
        f'{card_html(c["body"], esc)}'
        + (f'<p class="see">原文：<a href="{esc(c["see"])}">{esc(c["see"])}</a></p>' if c.get('see') and not c['see'].startswith('/ask/') else '')
        + '</article>' for c in cards)
    with open(os.path.join(out, 'ask', 'cards', 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(ctpl.replace('{{SITE_NAME}}', esc(site['name'])).replace('{{BASE}}', base).replace('{{YEAR}}', year)
                 .replace('{{CARDS}}', cards_html).replace('{{COUNT}}', str(len(cards))))

    # sitemap + llms.txt
    sm_path = os.path.join(out, 'sitemap.xml')
    if os.path.exists(sm_path):
        sm = open(sm_path, encoding='utf-8').read()
        add_urls = f"  <url><loc>{base}/ask/</loc><lastmod>{today}</lastmod></url>\n  <url><loc>{base}/ask/cards/</loc><lastmod>{today}</lastmod></url>\n"
        open(sm_path, 'w', encoding='utf-8').write(sm.replace('</urlset>', add_urls + '</urlset>'))
    llms_path = os.path.join(out, 'llms.txt')
    if os.path.exists(llms_path):
        with open(llms_path, 'a', encoding='utf-8') as fh:
            fh.write('\n## Ask\n\n'
                     f'- Ask Tianjie ({base}/ask/): an assistant that answers only from the public material on this site, citing a source for every paragraph.\n'
                     f'- Open context ({base}/ask/index.json): every source it may cite, as JSON.\n'
                     f'- Judgment cards ({base}/ask/cards/): short, dated statements with the conditions under which they hold.\n')

    return {'chunks': len(chunks), 'cards': len(cards), 'est_tokens': est, 'version': version}
