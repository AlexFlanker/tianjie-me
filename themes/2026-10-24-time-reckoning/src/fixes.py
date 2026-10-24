# -*- coding: utf-8 -*-
"""上线前核查后的改正：POST 替换表（原片段 → 新片段，构建时逐条报告命中次数）+ patch_data 数据补丁。"""
POST = [
]

def apply(page):
    report = []
    for i, (a, b, why) in enumerate(POST, 1):
        n = page.count(a)
        report.append(f'fix {i:02d} {"命中 ×" + str(n) if n else "未命中"}：{why}')
        if n: page = page.replace(a, b)
    return page, report

def patch_data(A, B, C, D):
    """改研究底稿里的数值 / 置信度；返回日志行。"""
    log = []
    return log
