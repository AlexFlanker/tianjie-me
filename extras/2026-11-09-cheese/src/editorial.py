# -*- coding: utf-8 -*-
"""号外 · 奶酪 — 中英文案（中文为主稿；事实只取自 research/*.json，改事实先改底稿）"""
def T(zh, en, **kw): d = {'zh': zh, 'en': en}; d.update(kw); return d

META = dict(
    slug='cheese', date='2026-11-09',
    title_zh='奶酪：让时间干活的七千年',
    title_en='Cheese: Seven Thousand Years of Letting Time Work',
    sub_zh='从安纳托利亚的陶罐讲到湾区的奶酪柜台：怎么来的、怎么做的、怎么尝、世界上别的地方怎么存奶。',
    sub_en='From Neolithic pots in Anatolia to a cheese counter in the Bay Area: where it came from, how it is made, how to taste it, and how the rest of the world keeps milk.',
    desc='关于奶酪的号外专题：七千年沿革，一块奶酪从一锅奶到熟成的工艺演示，品鉴光谱与风味轮，全球其他保存乳品的方式，以及湾区 Eataly、Whole Foods 奶酪柜台的导购。中英双语。',
)

HERO = dict(
    kick=T('号外 · 给 Daisy 与 Sichao', 'Extra · for Daisy & Sichao'),
    h1=T('奶会坏，<br>奶酪不会。', 'Milk spoils.<br>Cheese keeps.'),
    cta=T('从一只陶罐开始 ↓', 'Start with a pot ↓'),
)

NAV = [('hist', '00', T('沿革', 'History')), ('make', '01', T('做一块', 'Make')), ('taste', '02', T('品鉴', 'Taste')),
       ('world', '03', T('全球', 'World')), ('counter', '04', T('柜台', 'Counter')), ('end', '··', T('卷末', 'Notes'))]
