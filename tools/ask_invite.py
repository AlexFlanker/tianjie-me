#!/usr/bin/env python3
"""Make a signed invite link for /ask/ (recruiter / referrer mode, higher daily quota).

  INVITE_SECRET=... python3 tools/ask_invite.py --label "Acme · Jane (recruiter)" --days 30 --quota 30

The secret must equal the INVITE_SECRET variable set on the Cloudflare Pages project.
Tokens are stateless: to revoke every link, rotate INVITE_SECRET.
"""
import argparse, base64, hashlib, hmac, json, os, sys, time


def b64url(b):
    return base64.urlsafe_b64encode(b).decode().rstrip('=')


def make(secret, label, days, quota):
    payload = {'v': 1, 'l': label, 'e': int(time.time()) + days * 86400, 'q': quota}
    p = b64url(json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode('utf-8'))
    sig = b64url(hmac.new(secret.encode(), p.encode(), hashlib.sha256).digest())
    return f'{p}.{sig}'


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--label', required=True)
    ap.add_argument('--days', type=int, default=30)
    ap.add_argument('--quota', type=int, default=30)
    ap.add_argument('--base', default='https://tianjie.me')
    ap.add_argument('--secret', default=os.environ.get('INVITE_SECRET', ''))
    a = ap.parse_args()
    if not a.secret:
        sys.exit('set INVITE_SECRET (same value as on Cloudflare Pages) or pass --secret')
    tok = make(a.secret, a.label, a.days, a.quota)
    print(f"{a.base.rstrip('/')}/ask/?i={tok}")
