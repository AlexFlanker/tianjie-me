#!/usr/bin/env python3
"""Read what visitors asked and who left an email.

  ADMIN_TOKEN=... python3 tools/ask_admin.py inbox
  ADMIN_TOKEN=... python3 tools/ask_admin.py log --limit 20
  ADMIN_TOKEN=... python3 tools/ask_admin.py stats
"""
import argparse, json, os, sys, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument('kind', choices=['log', 'inbox', 'stats'])
ap.add_argument('--limit', type=int, default=50)
ap.add_argument('--base', default='https://tianjie.me')
a = ap.parse_args()
token = os.environ.get('ADMIN_TOKEN')
if not token:
    sys.exit('set ADMIN_TOKEN')
req = urllib.request.Request(f"{a.base.rstrip('/')}/api/admin?kind={a.kind}&limit={a.limit}", headers={'authorization': f'Bearer {token}', 'user-agent': 'tianjie-ask-admin/1.0'})  # Cloudflare blocks the default Python-urllib agent (error 1010)
data = json.load(urllib.request.urlopen(req, timeout=30))
if a.kind == 'stats':
    print(json.dumps(data, ensure_ascii=False, indent=2))
elif a.kind == 'inbox':
    for it in data['items']:
        print(f"{it['at'][:16]}  {it['email']}  {('[' + it['invite_label'] + '] ') if it.get('invite_label') else ''}{it.get('message', '')}")
        if it.get('question'):
            print(f"                  问题：{it['question']}")
else:
    for it in data['items']:
        r = it.get('receipt', {})
        print(f"{r.get('at', '')[:16]}  {r.get('verdict', ''):<9} {it.get('mode', ''):<9} {str(r.get('total_ms', '')):>6} ms  {it.get('q', '')[:70]}")
