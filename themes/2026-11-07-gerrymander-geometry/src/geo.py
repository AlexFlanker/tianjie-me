"""第 8 题的算法层（Python 版，与 geo.js 同公式，用于构建时预算与对拍）。

格子：N×N，cells[i] = 1 表示阵营 A（60 人），0 表示阵营 B（40 人）；plan[i] = 区号 0..K-1。
量尺：席位、浪费票、效率差（两种口径）、均值—中位数差、切边数、各区 Polsby–Popper（格子版）。
集合法：ReCom（合并相邻两区 → 随机生成树 → 找一条能把 2×20 格切成 20/20 的树边）。
分配：Hamilton / Jefferson / Adams / Webster / Dean / Huntington–Hill（最少 1 席）。
"""
import math, random
from collections import deque

# ---------------- 格子与邻接 ----------------
def neighbors(i, n):
    r, c = divmod(i, n)
    if r > 0: yield i - n
    if r < n - 1: yield i + n
    if c > 0: yield i - 1
    if c < n - 1: yield i + 1

def contiguous(plan, k, n):
    """每个区四邻连通？"""
    cells = [i for i in range(n * n) if plan[i] == k]
    if not cells: return False
    seen = {cells[0]}; dq = deque([cells[0]])
    while dq:
        i = dq.popleft()
        for j in neighbors(i, n):
            if plan[j] == k and j not in seen: seen.add(j); dq.append(j)
    return len(seen) == len(cells)

def valid(plan, n, K, size):
    cnt = [0] * K
    for p in plan: cnt[p] += 1
    return all(c == size for c in cnt) and all(contiguous(plan, k, n) for k in range(K))

# ---------------- 量尺 ----------------
def metrics(cells, plan, n, K):
    size = n * n
    a = [0] * K; tot = [0] * K
    for i in range(size):
        tot[plan[i]] += 1
        if cells[i]: a[plan[i]] += 1
    seatsA = sum(1 for k in range(K) if a[k] * 2 > tot[k])
    seatsB = sum(1 for k in range(K) if a[k] * 2 < tot[k])
    ties = K - seatsA - seatsB
    # 浪费票（Stephanopoulos & McGhee 2015）：输方全部票 + 赢方超过半数的票
    wA = wB = 0.0
    for k in range(K):
        half = tot[k] / 2
        b = tot[k] - a[k]
        if a[k] > b: wA += a[k] - half; wB += b
        elif b > a[k]: wB += b - half; wA += a[k]
        else: wA += a[k] - half; wB += b - half  # 平局：都算超出 0
    V = sum(cells) / size
    eg = (wB - wA) / size                      # 正值对 A 有利
    eg_simple = (seatsA / K - 0.5) - 2 * (V - 0.5)  # 各区同等大小时与上式一致
    shares = sorted(a[k] / tot[k] for k in range(K))
    med = shares[K // 2] if K % 2 else (shares[K // 2 - 1] + shares[K // 2]) / 2
    mean = sum(shares) / K
    mm = med - mean                            # 正值对 A 有利（A 的中位区比平均区更强）
    cut = 0
    for i in range(size):
        r, c = divmod(i, n)
        if c < n - 1 and plan[i] != plan[i + 1]: cut += 1
        if r < n - 1 and plan[i] != plan[i + n]: cut += 1
    pp = []
    for k in range(K):
        area = tot[k]; per = 0
        for i in range(size):
            if plan[i] != k: continue
            r, c = divmod(i, n)
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                rr, cc = r + dr, c + dc
                if rr < 0 or rr >= n or cc < 0 or cc >= n or plan[rr * n + cc] != k: per += 1
        pp.append(4 * math.pi * area / (per * per) if per else 0)
    return dict(seatsA=seatsA, seatsB=seatsB, ties=ties, aVotes=a, tot=tot, wastedA=wA, wastedB=wB, eg=eg, egSimple=eg_simple,
                meanMedian=mm, shares=shares, cutEdges=cut, pp=pp, ppMean=sum(pp) / K)

# ---------------- ReCom ----------------
def _spanning_tree(nodes, n, rng):
    """随机生成树（随机权重 Kruskal 等价于随机 BFS 顺序的 Prim）。返回父表。"""
    nodes = list(nodes); inset = set(nodes)
    start = rng.choice(nodes)
    parent = {start: None}; frontier = [start]; order = []
    # Wilson 太慢；用「随机 DFS/BFS 混合」：随机挑前沿边
    edges = [(start, j) for j in neighbors(start, n) if j in inset]
    while edges:
        idx = rng.randrange(len(edges)); u, v = edges[idx]; edges[idx] = edges[-1]; edges.pop()
        if v in parent: continue
        parent[v] = u
        for j in neighbors(v, n):
            if j in inset and j not in parent: edges.append((v, j))
    return parent

def recom_step(plan, n, K, size, rng, tries=30):
    """合并两个相邻区，重新一分为二（各恰 size 格，连通）。失败返回 None。"""
    for _ in range(tries):
        # 找一条跨区边
        i = rng.randrange(n * n)
        nb = [j for j in neighbors(i, n) if plan[j] != plan[i]]
        if not nb: continue
        j = rng.choice(nb); k1, k2 = plan[i], plan[j]
        nodes = [x for x in range(n * n) if plan[x] in (k1, k2)]
        parent = _spanning_tree(nodes, n, rng)
        if len(parent) != len(nodes): continue
        # 子树大小
        children = {u: [] for u in parent}
        root = None
        for v, u in parent.items():
            if u is None: root = v
            else: children[u].append(v)
        sub = {}
        order = []; stack = [root]
        while stack:
            u = stack.pop(); order.append(u); stack.extend(children[u])
        for u in reversed(order): sub[u] = 1 + sum(sub[c] for c in children[u])
        cands = [v for v in parent if parent[v] is not None and sub[v] == size]
        if not cands: continue
        v = rng.choice(cands)
        # 以 v 为根的子树成为一区
        part = set(); stack = [v]
        while stack:
            u = stack.pop(); part.add(u); stack.extend(children[u])
        new = list(plan)
        a, b = (k1, k2) if rng.random() < 0.5 else (k2, k1)
        for x in nodes: new[x] = a if x in part else b
        return new
    return None

def strips(n, K):
    """初始方案：K 条横带。"""
    size = n * n // K
    return [min(K - 1, i // size) for i in range(n * n)]

def ensemble(cells, plan, n, K, steps, seed=1, burn=0):
    rng = random.Random(seed); cur = plan; out = []
    size = n * n // K
    for s in range(steps + burn):
        nxt = recom_step(cur, n, K, size, rng)
        if nxt is not None: cur = nxt
        if s >= burn:
            m = metrics(cells, cur, n, K)
            out.append((m['seatsA'], m['eg'], m['cutEdges'], cur))
    return out

def search_target(cells, n, K, seatsA_target, rng, steps=4000, start=None, want_compact=False):
    """用 ReCom 走链 + 目标函数的简单退火找到指定席位数的方案。"""
    size = n * n // K
    cur = start or strips(n, K)
    def score(p):
        m = metrics(cells, p, n, K)
        s = abs(m['seatsA'] - seatsA_target) * 100 + m['ties'] * 100
        # 第二目标：席位到位后尽量紧凑（或尽量不紧凑），用切边数
        s += m['cutEdges'] * (1 if want_compact else -0.3)
        return s, m
    cs, cm = score(cur); best = (cs, cur, cm)
    T = 30.0
    for s in range(steps):
        nxt = recom_step(cur, n, K, size, rng)
        if nxt is None: continue
        ns, nm = score(nxt)
        if ns <= cs or rng.random() < math.exp((cs - ns) / T):
            cur, cs, cm = nxt, ns, nm
            if cs < best[0]: best = (cs, cur, cm)
        T = max(0.5, T * 0.999)
    return best

# ---------------- 分配 ----------------
def hamilton(pops, H, minimum=1):
    tot = sum(pops); q = [p / tot * H for p in pops]
    seats = [max(minimum, int(math.floor(x))) for x in q]
    rem = H - sum(seats)
    order = sorted(range(len(pops)), key=lambda i: (-(q[i] - seats[i]), i))
    for i in order[:max(0, rem)]: seats[i] += 1
    return seats

def divisor(pops, H, method, minimum=1):
    """除数法用「优先值」逐席分配：每州先给 minimum 席，之后第 s+1 席的优先值 = pop / d(s)。"""
    def d(s):
        if method == 'jefferson': return s + 1
        if method == 'adams': return s
        if method == 'webster': return s + 0.5
        if method == 'dean': return s * (s + 1) / (s + 0.5)   # 调和平均
        if method == 'huntington_hill': return math.sqrt(s * (s + 1))
        raise ValueError(method)
    n = len(pops); seats = [minimum] * n
    for _ in range(H - minimum * n):
        best = None; bi = -1
        for i in range(n):
            s = seats[i]
            den = d(s)
            pv = float('inf') if den == 0 else pops[i] / den
            if best is None or pv > best: best, bi = pv, i
        seats[bi] += 1
    return seats

def apportion(pops, H, method, minimum=1):
    return hamilton(pops, H, minimum) if method == 'hamilton' else divisor(pops, H, method, minimum)

# ---------------- 席位—选票曲线 ----------------
def seats_share(v, k=3.0, bias=0.0):
    """S/(1−S) = ((V+bias)/(1−V−bias))^k；bias 是把曲线左右平移的偏置（对 A 有利为正）。"""
    v = min(0.999, max(0.001, v + bias))
    r = (v / (1 - v)) ** k
    return r / (1 + r)
