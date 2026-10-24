"""用 PyEphem 按 GB/T 33661-2017 的规则（北京时间 UTC+8 为日界、冬至所在月为十一月、无中气置闰）生成 1899–2101 年农历月表。
输出 src/lunar_table.json：{"<农历年>": [正月初一的 JDN, 闰月序号(0=无; n=闰 n 月), "每月大小串(1=30 天,0=29 天)"]}
"""
import ephem, json, datetime as dt, math, sys, os
BJ = dt.timedelta(hours=8)
def to_bj_date(e):  # ephem.Date -> 北京日期
    return (ephem.Date(e).datetime() + BJ).date()
def jdn(d):  # 公历日期 -> JDN
    a=(14-d.month)//12; y=d.year+4800-a; m=d.month+12*a-3
    return d.day+(153*m+2)//5+365*y+y//4-y//100+y//400-32045
# 1. 朔日
moons=[]; t=ephem.Date('1897/11/1')
while t < ephem.Date('2102/6/1'):
    t=ephem.next_new_moon(t); moons.append(to_bj_date(t)); t=ephem.Date(t+1)
# 2. 中气（太阳黄经 = 30°k）；冬至 = 270°
def sun_lon(e):
    s=ephem.Sun(e); return math.degrees(ephem.Ecliptic(s, epoch=e).lon) % 360
def find_lon(target, start):  # 从 start 起找太阳黄经达到 target 的时刻（二分）
    lo=ephem.Date(start); hi=ephem.Date(lo+40)
    def f(e): return ((sun_lon(e)-target+180)%360)-180
    # 保证 f(lo)<0<f(hi)
    while f(lo)>0: lo=ephem.Date(lo-5)
    while f(hi)<0: hi=ephem.Date(hi+5)
    for _ in range(50):
        mid=ephem.Date((lo+hi)/2)
        if f(mid)<0: lo=mid
        else: hi=mid
    return hi
zhongqi={}  # date -> k (0..11), k=0 冬至? 用黄经 k*30
t=ephem.Date('1897/12/1')
while t < ephem.Date('2102/6/1'):
    lon=sun_lon(t); k=int(lon//30)+1; target=(k*30)%360
    t=find_lon(target, t); zhongqi[to_bj_date(t)]=target; t=ephem.Date(t+20)
solstices=sorted(d for d,l in zhongqi.items() if l==270)
# 3. 建月
def month_has_zq(start, end):
    return any(start<=d<end for d in zhongqi)
months=[]  # (start_date, number, leap)
for i in range(len(solstices)-1):
    s0, s1 = solstices[i], solstices[i+1]
    # 冬至所在月：最后一个朔日 <= s0
    idx0=max(j for j,m in enumerate(moons) if m<=s0); idx1=max(j for j,m in enumerate(moons) if m<=s1)
    n=idx1-idx0  # 两个十一月之间的月数（12 或 13）
    leap_done=False; num=11
    for j in range(idx0, idx1):
        st, en = moons[j], moons[j+1]
        if j==idx0: months.append((st,11,False)); num=11; continue
        if n==13 and not leap_done and not month_has_zq(st,en):
            months.append((st,num,True)); leap_done=True; continue
        num = num%12+1; months.append((st,num,False))
# 4. 按农历年打包（正月起）
table={}
starts=[k for k,m in enumerate(months) if m[1]==1 and not m[2]]
for a,b in zip(starts, starts[1:]):
    ms=months[a:b]; y=ms[0][0].year
    bits=''.join('1' if (ms[k+1][0]-ms[k][0]).days==30 else '0' for k in range(len(ms)-1))
    bits+= '1' if (months[b][0]-ms[-1][0]).days==30 else '0'
    leap=next((m[1] for m in ms if m[2]),0)
    table[str(y)]=[jdn(ms[0][0]), leap, bits]
json.dump(table, open(os.path.join(os.path.dirname(__file__),'..','lunar_table.json'),'w'), separators=(',',':'))
# 5. 对拍
def cny(y): 
    j=table[str(y)][0]; # JDN -> date
    a=j+32044; b=(4*a+3)//146097; c=a-146097*b//4; d=(4*c+3)//1461; e=c-1461*d//4; m=(5*e+2)//153
    return dt.date(100*b+d-4800+m//10, m+3-12*(m//10), e-(153*m+2)//5+1)
checks={2023:'2023-01-22',2024:'2024-02-10',2025:'2025-01-29',2026:'2026-02-17',2027:'2027-02-06',1985:'1985-02-20',2007:'2007-02-18',1900:'1900-01-31',2000:'2000-02-05',2033:'2033-01-31',2034:'2034-02-19'}
ok=True
for y,s in checks.items():
    got=str(cny(y)); print(y, got, 'OK' if got==s else 'MISMATCH vs '+s); ok&=got==s
for y,l in {2017:6,2020:4,2023:2,2025:6,2024:0,2026:0,2027:0,2033:11,2014:9}.items():
    print(y,'leap',table[str(y)][1],'OK' if table[str(y)][1]==l else 'MISMATCH vs %d'%l); ok&=table[str(y)][1]==l
print('years', len(table), 'ALL OK' if ok else 'CHECK FAILED')
