#!/usr/bin/env python3
"""把研究底稿（research/*.json）与编辑文案合成 content.json，供 build_theme.py 注入页面。"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.environ.get('DANCE_RESEARCH', '/tmp/claude-0/-home-claude/4c860612-bdf6-56ce-80cf-1843e1d1c566/scratchpad/dance-build/research')

def load(name):
    return json.load(open(os.path.join(R, name), encoding='utf-8'))

nodes = load('nodes_1_8.json') + load('nodes_9_12.json')
decks = load('decks.json'); works = load('works.json'); quick = load('quick.json')
images = json.load(open(os.path.join(HERE, 'images.json'), encoding='utf-8'))

# ---------- 图版与图注（文件名 → 节点） ----------
CAPTIONS = {
 'n01': ('舞蹈纹彩陶盆', '马家窑文化，青海大通上孙家寨 1973 年出土，中国国家博物馆藏。内壁三组各五人，手拉手、头饰与尾饰向同一侧摆动。'),
 'n02': ('曾侯乙编钟', '战国早期，1978 年湖北随州出土，湖北省博物馆藏。钟磬是雅乐六代舞的伴奏主体。'),
 'n03': ('汉画像砖 · 乐舞百戏', '东汉画像砖上的乐舞与杂技：盘鼓、长袖、俳优同台，是舞蹈第一次成为职业表演的实物记录。'),
 'n04': ('莫高窟第 285 窟 · 飞天', '西魏（535–557）。佛教伎乐把西域乐器与飞舞的身姿画进了敦煌。'),
 'n05': ('莫高窟中唐壁画 · 胡旋与琵琶', '中唐（吐蕃时期，781–848）壁画局部：旋转的舞者与大琵琶，丝路乐舞在盛唐之后仍是宫廷与寺窟的常客。'),
 'n06': ('《大傩图》轴', '宋，佚名，故宫博物院藏。十二人戴面具、执器物作舞，是乡傩与「舞队」的珍贵图像。'),
 'n07': ('元代杂剧壁画', '山西洪洞广胜寺明应王殿壁画（1324），题榜「大行散乐忠都秀在此作场」——舞蹈进入戏曲舞台的直接证据。'),
 'n08': ('《明宪宗元宵行乐图》局部', '明，佚名，中国国家博物馆藏。元宵节宫中的杂耍与社火队伍，民间游艺进入宫廷的年节。'),
 'n09': ('1945 年 · 群众扭秧歌庆祝抗战胜利', '延安新秧歌运动之后，秧歌从田间节庆变成了全民的庆典语言。'),
 'n10': ('1953 年 · 中国青年艺术团的舞者', '德国摄影档案（Deutsche Fotothek）里的中国青年艺术团演出，手持荷灯的队形与同年获奖的《荷花舞》气质相近。'),
 'n11': ('莫高窟九层楼', '1979 年《丝路花雨》让敦煌壁画里的舞姿「活」成一个舞种，此后「敦煌舞」成为中国古典舞的一支。'),
 'n12': ('正月里的秧歌', '今天的秧歌仍是北方正月最常见的街头舞蹈；短视频时代，它的一个动作就能被几亿人看见。'),
 'deck-hgd': ('淮河 · 蚌埠', '花鼓灯的故乡：淮河两岸雨多土黏，「天上下雨地下滑」练出了闪身步的应变。'),
 'deck-gz': ('秧歌队的街头表演', '秧歌是北方最普遍的节庆舞，鼓子秧歌是其中最阳刚的一支（图为 2025 年国庆的一支秧歌队，非鼓子秧歌，示意）。'),
}
def credit(tag):
    im = images[tag]; cap = CAPTIONS[tag]
    author = im['author'] or '佚名'
    if tag == 'n10': author = 'Roger & Renate Rössing / Deutsche Fotothek'
    if tag == 'n06': author = '佚名（宋）'
    if tag == 'n07': author = '佚名（元）'
    if tag == 'n08': author = '佚名（明）'
    if tag == 'n09': author = '不详（1945）'
    lic = im['license'] or 'Public domain'
    return {'src': f'assets/{tag}.jpg', 'w': im['w'], 'h': im['h'], 'title': cap[0], 'caption': cap[1], 'author': author, 'license': lic, 'license_link': im.get('license_link', ''), 'page': im['page']}

for n in nodes:
    n['image'] = credit(n['id'])
    n['facts'] = n.get('facts', [])[:7]

# ---------- 爆梗现场时间线（9/22–10/2） ----------
meme = {
 'intro': '2026 年 9 月下旬，两段北京舞蹈学院的民族民间舞专业教学视频被网友「考古」翻出：一段是赵铁春教授示范的安徽花鼓灯「闪身步」，一段是明文军教授示范的山东鼓子秧歌「狗熊哆嗦毛」。诙谐的动作名、一本正经的示范、两项国家级非遗——三件事凑在一起，成了这个秋天最大的舞蹈梗。',
 'events': [
  {'d': '9/22 前后', 't': '教学视频在短视频平台被翻出，「闪身步」「浪子踢球」「狗熊哆嗦毛」开始刷屏。', 's': '中华网 9/24', 'u': 'https://news.china.com/socialgd/10000169/20260924/49763238.html'},
  {'d': '9/24', 't': '中华网统计相关视频播放量超 6 亿；课程录制人赵铁春回应：「出圈是意料之外，也是意料之中。」同日，81 岁花鼓灯国家级传承人娄楼：「闪身步只是花鼓灯几百个动作里的一个，欢迎大家来安徽看原汁原味的花鼓灯。」', 's': '中华网 · 凤凰网安徽', 'u': 'https://ah.ifeng.com/c/8wfxR8S9AG0'},
  {'d': '9/24–25', 't': '闫妮、周笔畅、杨迪、汪苏泷、李一桐（北舞民间舞系出身）等接力模仿；媒体与医生提醒别盲目跟跳。', 's': '凤凰网安徽 · 腾讯新闻', 'u': 'https://view.inews.qq.com/a/20260925A05FQC00'},
  {'d': '9/27', 't': '名古屋亚运会花样游泳双人冠军林彦君、徐汇妍与林彦含在颁奖礼后跳闪身步；国羽女队颁奖时集体「闪」。', 's': '新浪新闻', 'u': 'https://k.sina.com.cn/article_7879995911_1d5af320706802nxam.html'},
  {'d': '9/28', 't': '舞剧《大染坊》2.0 版在济南开演，谢幕用鼓子秧歌复刻「狗熊哆嗦毛」；据搜狐当日统计，相关视频播放量已超 7.5 亿（各家口径不一：中华网 9/24 称 6 亿，腾讯 9/27 称 7 亿）。', 's': '央视新闻 · 搜狐', 'u': 'https://sohu.com/a/1080711873_121443915'},
  {'d': '9/29', 't': '澎湃《怎么就突然火了》：传承人冯太新说花鼓灯主要靠家族传承、面临现实困境，欢迎年轻人来跳、来翻拍，让花鼓灯走出安徽。', 's': '澎湃 · 虎嗅', 'u': 'https://m.thepaper.cn/newsDetail_forward_34158213'},
  {'d': '10/1', 't': '光明网：「狗熊哆嗦毛」出自《山东秧歌舞蹈（基础）训练教材》，要领「稳、沉、抻、韧」，口令「隆咚框隆咚框隆咚隆咚隆咚框」。', 's': '光明网', 'u': 'https://difang.gmw.cn/sd/2026-10/01/content_39030430.htm'},
  {'d': '10/2', 't': '澎湃：北舞教授田露讲述当年教材录制往事——这些视频本是给专业学生的训练片。', 's': '澎湃新闻', 'u': 'https://www.thepaper.cn/newsDetail_forward_34191454'},
 ],
 'pair': [
  {'who': '赵铁春', 'role': '中国舞蹈家协会副主席、国家大剧院副院长（2016 年起），北京舞蹈学院教授；曾任北舞中国民族民间舞系主任、副院长', 'what': '安徽花鼓灯「闪身步」', 'material': '《安徽花鼓灯（男班）》教材视频，2018 年前后录制', 'heritage': '花鼓灯 · 国家级非遗 Ⅲ-6（2006 第一批）', 'quote': '这个动作有中国民间传统文化的特征，同时有大众传播性。大家觉得好玩、有梗，有幽默感又有专业性，这种趣味现象是大众群体的创造。'},
  {'who': '明文军', 'role': '北京舞蹈学院教授；曾任北舞副院长、文化和旅游部艺术司司长', 'what': '山东鼓子秧歌「狗熊哆嗦毛」', 'material': '《山东秧歌舞蹈（基础）训练教材》教学视频，录制年份 2001 / 2018 两说', 'heritage': '秧歌（商河鼓子秧歌）· 国家级非遗 Ⅲ-2（2006 第一批）', 'quote': '稳、沉、抻、韧——发力要稳、重心要沉、动作要抻、劲儿要韧。'},
 ],
}

# ---------- 教材卡组：整理字段、选出有动态小人的三张 ----------
FIG = {'闪身步': 'shan', '浪子踢球': 'langzi', '狗熊哆嗦毛': 'dou'}
def tidy_deck(d, key):
    out = {k: d.get(k) for k in ('name', 'heritage', 'region', 'roles', 'scenes', 'schools', 'teacher', 'inheritors', 'sources')}
    out['key'] = key
    full, names_only = [], []
    for m in d['moves']:
        m = dict(m); m['fig'] = FIG.get(m['name'].split('（')[0])
        how = (m.get('how') or '').strip()
        if m.get('confidence') == '低' or (not how or how.startswith('仅见') or how.startswith('要领未')) and not m['fig']:
            names_only.append(m['name'])
        else:
            full.append(m)
    out['moves'] = full; out['names_only'] = names_only
    return out
hgd = tidy_deck(decks['huagudeng'], 'huagudeng'); gz = tidy_deck(decks['guzi'], 'guzi')
hgd['image'] = credit('deck-hgd')

# 把闪身步归属两说、浪子踢球改成已核口径
for m in hgd['moves']:
    if m['name'].startswith('闪身步'):
        m['role'] = '兰花躲鼓架子逗趣时的闪避（金明、张小春口径一致）；教学原片出自男班教材，由男老师示范'
        m['cue'] = '溜得快、刹得住'
        m['how'] = '腰腹发力，肩头错动，重心瞬间平移；脚贴着地面滑出去，再急停——像瞬间躲开什么。分侧闪、前闪、后闪。'
        m['life'] = '淮河两岸雨多、土黏，「天上下雨地下滑，一摔摔个仰八叉」——雨地里走路练出的应变，被编进了舞步。'
        m['scene'] = '小花场 · 双人逗趣'
    if m['name'].startswith('浪子踢球'):
        m['how'] = '踢的是女角「兰花」鞋尖上的绣球：脚尖一挑一踢，带动全身的协调；传承人金明称其为兰花戏剧化表现「嗔怒」的基本动作。'
        m['life'] = '兰花的绣花鞋与鞋尖绣球是淮河民俗里的装扮，踢球是把装扮变成了身段。'
        m['scene'] = '小花场 · 双人逗趣'
        m['cue'] = m.get('cue') or '一挑、一踢、一收'
for m in gz['moves']:
    if m['name'].startswith('狗熊哆嗦毛'):
        m['cue'] = '隆咚框 隆咚框 隆咚隆咚隆咚框'
        m['how'] = '以腰腹先带动大臂，力量顺势传到全身，膝盖持续屈伸颤动，配合鼓子秧歌标志性的十字步；全程「稳、沉、抻、韧」。原片里是一句七秒的完整乐句：起势、横扫成弓步、双臂举过头顶往下抖落、展臂、收势。'
        m['life'] = '黄河岸边庄稼汉的粗犷劲儿——像狗熊抖落一身毛，看着憨，力量感十足。'
        m['scene'] = '跑场子 · 鼓子群舞'

# ---------- 鉴赏对照：去掉无来源的传闻行，保留低置信但有出处的 ----------
rows = []
for r in works:
    if '传闻' in (r.get('work') or '') or r.get('confidence') == '低' and not (r.get('link') or r.get('source')):
        continue
    rows.append(r)

# ---------- 参考（按章分组）----------
refs = {
 '一 · 爆梗现场': [{'t': e['s'], 'u': e['u']} for e in meme['events']] + [
   {'t': '虎嗅：全网爆梗「狗熊哆嗦毛」和闪身步，司长看了都叫好', 'u': 'https://www.huxiu.com/article/4894038.html'},
   {'t': '搜狐：「闪身步」全网刷屏，原来这个动作来自安徽花鼓灯（金明访谈）', 'u': 'https://www.sohu.com/a/1082433896_121124574'},
   {'t': '搜狐：花鼓灯资深演员张小春揭秘舞步源自生活', 'u': 'https://www.sohu.com/a/1080571120_120952561'}],
 '二 · 从劳作到艺术': [{'t': f"{f['source']}", 'u': f.get('url', '')} for n in nodes for f in n['facts'] if f.get('url')],
 '三 · 动作教材': [{'t': s, 'u': s if s.startswith('http') else ''} for s in (hgd.get('sources') or [])] + [{'t': s, 'u': s if s.startswith('http') else ''} for s in (gz.get('sources') or [])],
 '四 · 鉴赏对照': [{'t': f"{r['work']}（{r.get('troupe') or ''}）", 'u': r.get('link') or ''} for r in rows if r.get('link')] + [{'t': q.get('source', ''), 'u': ''} for q in quick if q.get('source')],
}
# 去重
for k in refs:
    seen = set(); uniq = []
    for x in refs[k]:
        key = (x['t'], x['u'])
        if key in seen or not x['t']: continue
        seen.add(key); uniq.append(x)
    refs[k] = uniq

content = {
 'title': '舞从劳作来', 'subtitle': '从「百兽率舞」到「闪身步」——中国版图上五千年的舞蹈沉淀图谱',
 'thesis': '每个爆梗的动作背后，都是一方水土几百年的生产生活。',
 'steps': ['看地图上的十二个时代图层', '翻北舞两位老师的动作卡', '带着对照表去看演出'],
 'meme': meme, 'nodes': nodes, 'decks': [hgd, gz], 'works': rows, 'quick': quick,
 'why': {
  'paras': [
   '短视频把「动作」从「作品」里拆了出来。过去我们看一支舞，看的是一台节目、一部舞剧；现在被几亿人看见的是三秒钟的一个步法，名字还很好笑。这不是第一次——2023 年的「科目三」也是这样——但这一次被翻出来的，是两项国家级非遗的专业训练片。',
   '为什么是闪身步和狗熊哆嗦毛？因为它们恰好站在两个极端上：一个是淮河两岸雨地里练出来的应变，溜得快、刹得住；一个是黄河岸边庄稼汉的憨直劲儿，稳、沉、抻、韧。一个躲，一个抖，都是身体对土地的记忆，也都好学、好笑、好拍。',
   '传承人的态度是欢迎的——「闪身步只是花鼓灯几百个动作里的一个」，娄楼老人说，欢迎大家来安徽看原汁原味的花鼓灯；冯太新则提醒，这项非遗主要靠家族传承，面临现实困境，年轻人来跳、来翻拍，是在帮它走出安徽。另一面是医生的提醒：膝关节侧向受力，量力而行。',
   '所以这一题没有停在梗上。往前翻五千年，舞蹈一直是这样从劳作、仪式和交融里沉淀下来的——「百兽率舞」是狩猎，车水步是浇田，胡旋是丝路，秧歌是农事与年节。看懂了这条线，再回去看那三秒钟的闪身步，你看到的就不只是一个梗。',
  ],
 },
 'method': {
  'items': [
   '时间轴十二个节点的事实每条标出处与置信度（高 / 中 / 低）：高 = 原典或官方条目直接支持；中 = 报道转述或仅一处来源；低 = 仅有名称或年代存疑。有争议处把两说并列，不替读者选边。',
   '动作教材以两位老师的教学原片与媒体报道为准，要领未见原话的动作只列名字，不编要领；「风险」一栏是编辑提示，不是专家原话。',
   '页面上的墨线小人由一副 7.5 头身的二维骨架驱动：闪身步、浪子踢球、狗熊哆嗦毛三个动作的骨架数据来自两段教学原片（MediaPipe 逐帧提取 33 个关节点，映射到同一副骨架，15 fps 平滑后循环）。原片只用于提取骨架坐标，页面不出现任何视频画面；胯横移与手臂角做了约 15–20% 的可读性夸张。',
   '地图按现行省级行政区划绘制；各时代的高亮与路线是文化传播示意，不是政区图。图片均来自 Wikimedia Commons 的公有领域或 CC 授权文件，图注里给出作者与许可证。',
   '鉴赏对照表只给官方渠道（文旅部、院团、央视网），不嵌第三方视频；查不到官方链接的只写作品名。',
  ],
  'todo': ['鼓子秧歌教材录制年份（2001 / 2018）', '视频播放量的统计口径（6 / 7 / 7.5 亿）', '《淮水情兰花弯》首演年份与获奖', '历年春晚中的花鼓灯 / 鼓子秧歌节目', '鼓子秧歌国家级代表性传承人名单', '花鼓灯教材中「挂鞭推车」等九个动作的要领'],
 },
 'refs': refs,
 'credits': {k: credit(k) for k in CAPTIONS},
 'generated': '2026-10-03',
}
json.dump(content, open(os.path.join(HERE, 'content.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('content.json written:', 'nodes', len(nodes), 'hgd moves', len(hgd['moves']), '+', len(hgd['names_only']), 'names; gz moves', len(gz['moves']), '+', len(gz['names_only']), '; works', len(rows), '; quick', len(quick))
