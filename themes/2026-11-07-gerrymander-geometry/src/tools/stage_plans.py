"""序章与画线器用的选民格子与五张预置划法；顺带对拍研究员 C 的 demo_grid。"""
import json, random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import geo
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(os.path.join(HERE, 'research', 'metrics_C.json'), encoding='utf-8'))
n, K = 10, 5
# 对拍 C 的三张图
g = C['demo_grid']
for pid, p in g['plans'].items():
    plan = [0] * 100
    for k, d in enumerate(p['districts']):
        for i in d['cells']: plan[i] = k
    assert geo.valid(plan, n, K, 20), pid
    m = geo.metrics(g['cells'], plan, n, K)
    print('C 对拍', pid, 'seatsA', m['seatsA'], 'eg', round(m['eg'], 3), 'mm', round(m['meanMedian'], 3), 'wA/wB', m['wastedA'], m['wastedB'], '| C 写', p['seats_A'], p['efficiency_gap_A'], p['mean_median_A'], p['wasted_A'], p['wasted_B'])

# 本题的选民图：B（0）是一座「城」：中部偏左的团块 + 零星几户；A（1）是周围的「乡」。
rows = [
 "1111111111",
 "1110011111",
 "1100000111",
 "1000000011",
 "1000000011",
 "1000000011",
 "1100000111",
 "1110000111",
 "1111001101",
 "1111111111",
]
cells = [int(ch) for r in rows for ch in r]
assert len(cells) == 100 and sum(cells) == 60, sum(cells)
rng = random.Random(8)
plans = {}
# 3:2 紧凑（公平的参考）
s, plan32, m = geo.search_target(cells, n, K, 3, rng, steps=6000, want_compact=True); plans['fair'] = plan32; print('fair', m['seatsA'], m['cutEdges'], round(m['eg'],3))
# 5:0 拆
s, plan50, m = geo.search_target(cells, n, K, 5, rng, steps=8000); plans['crack'] = plan50; print('crack', m['seatsA'], m['cutEdges'], round(m['eg'],3))
# 4:1 塞：一个区尽量全是 B
def score_pack(p):
    m = geo.metrics(cells, p, n, K); worst = max(20 - a for a in m['aVotes'])  # 最多 B 的区
    return abs(m['seatsA'] - 4) * 100 + m['ties'] * 100 - worst * 3 + m['cutEdges'] * 0.5, m
cur = plan32; cs, cm = score_pack(cur); best = (cs, cur, cm); T = 20
for i in range(8000):
    nxt = geo.recom_step(cur, n, K, 20, rng)
    if nxt is None: continue
    ns, nm = score_pack(nxt)
    if ns <= cs or rng.random() < math.exp((cs - ns) / T): cur, cs, cm = nxt, ns, nm
    if cs < best[0]: best = (cs, cur, cm)
    T = max(0.5, T * 0.999)
plans['pack'] = best[1]; print('pack', best[2]['seatsA'], best[2]['cutEdges'], round(best[2]['eg'],3), 'B in packed', max(20 - a for a in best[2]['aVotes']))
# 2:3 反转
s, plan23, m = geo.search_target(cells, n, K, 2, rng, steps=8000); plans['flip'] = plan23; print('flip', m['seatsA'], m['cutEdges'], round(m['eg'],3))
# 随机一张：从条带起跑链 1500 步后取一张
ens = geo.ensemble(cells, geo.strips(n, K), n, K, 3000, seed=11, burn=500)
hist = {}
for sa, eg, cut, p in ens: hist[sa] = hist.get(sa, 0) + 1
print('ensemble seatsA hist', dict(sorted(hist.items())), 'mean eg', round(sum(e for _, e, _, _ in ens) / len(ens), 3))
plans['random'] = ens[1234][3]
for k, p in plans.items(): assert geo.valid(p, n, K, 20), k
out = {'n': n, 'K': K, 'cells': cells, 'plans': {k: p for k, p in plans.items()}, 'metrics': {k: geo.metrics(cells, p, n, K) for k, p in plans.items()},
       'ensemble': {'steps': 3000, 'burn': 500, 'seed': 11, 'hist': {str(k): v for k, v in sorted(hist.items())}, 'egs': [round(e, 3) for _, e, _, _ in ens], 'cuts': [c for _, _, c, _ in ens]}}
json.dump(out, open(os.path.join(HERE, 'stage.json'), 'w', encoding='utf-8'), ensure_ascii=False)
for k, p in plans.items():
    print(k); 
    for r in range(n): print(' ', ''.join(str(p[r*n+c]) for c in range(n)), ' ', ''.join('A' if cells[r*n+c] else '.' for c in range(n)))
