# -*- coding: utf-8 -*-
"""核查后的改正：POST 替换表（成品页逐条替换并报告是否命中）+ patch_data（直接改研究底稿的字段）。"""
POST = [
    # ('原片段', '新片段'),
]
def patch_data(A, B, C, D):
    out = []
    return out
def apply(page):
    report = []
    for old, new in POST:
        n = page.count(old)
        if n: page = page.replace(old, new)
        report.append(f'{"ok  " if n else "MISS"} ×{n} {old[:60]}')
    return page, report
