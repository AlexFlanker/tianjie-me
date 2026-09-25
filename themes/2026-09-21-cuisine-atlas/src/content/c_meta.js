const DATA = { periods: [], provinces: {}, families: {}, tastes: {}, staples: {}, provNotes: {}, modern: {}, refs: [] };

// 34 省级行政区：name 全称简写、short 简称、label 地图标签、dx/dy 标签偏移（相对几何中心）
DATA.provinces = {
  BJ:{name:'北京', short:'京', label:'北京', dx:-14, dy:-16},
  TJ:{name:'天津', short:'津', label:'天津', dx:24, dy:13},
  HE:{name:'河北', short:'冀', label:'河北', dx:-4, dy:22},
  SX:{name:'山西', short:'晋', label:'山西', dx:0, dy:0},
  NM:{name:'内蒙古', short:'蒙', label:'内蒙古', dx:0, dy:0},
  LN:{name:'辽宁', short:'辽', label:'辽宁', dx:0, dy:0},
  JL:{name:'吉林', short:'吉', label:'吉林', dx:0, dy:0},
  HL:{name:'黑龙江', short:'黑', label:'黑龙江', dx:0, dy:0},
  SH:{name:'上海', short:'沪', label:'上海', dx:22, dy:4},
  JS:{name:'江苏', short:'苏', label:'江苏', dx:0, dy:0},
  ZJ:{name:'浙江', short:'浙', label:'浙江', dx:0, dy:0},
  AH:{name:'安徽', short:'皖', label:'安徽', dx:0, dy:0},
  FJ:{name:'福建', short:'闽', label:'福建', dx:0, dy:0},
  JX:{name:'江西', short:'赣', label:'江西', dx:0, dy:0},
  SD:{name:'山东', short:'鲁', label:'山东', dx:0, dy:0},
  HA:{name:'河南', short:'豫', label:'河南', dx:0, dy:0},
  HB:{name:'湖北', short:'鄂', label:'湖北', dx:0, dy:0},
  HN:{name:'湖南', short:'湘', label:'湖南', dx:0, dy:0},
  GD:{name:'广东', short:'粤', label:'广东', dx:-6, dy:-6},
  GX:{name:'广西', short:'桂', label:'广西', dx:0, dy:0},
  HI:{name:'海南', short:'琼', label:'海南', dx:0, dy:0},
  CQ:{name:'重庆', short:'渝', label:'重庆', dx:0, dy:0},
  SC:{name:'四川', short:'川', label:'四川', dx:0, dy:0},
  GZ:{name:'贵州', short:'黔', label:'贵州', dx:0, dy:0},
  YN:{name:'云南', short:'滇', label:'云南', dx:0, dy:0},
  XZ:{name:'西藏', short:'藏', label:'西藏', dx:0, dy:0},
  SN:{name:'陕西', short:'陕', label:'陕西', dx:0, dy:0},
  GS:{name:'甘肃', short:'甘', label:'甘肃', dx:0, dy:0},
  QH:{name:'青海', short:'青', label:'青海', dx:0, dy:0},
  NX:{name:'宁夏', short:'宁', label:'宁夏', dx:0, dy:0},
  XJ:{name:'新疆', short:'新', label:'新疆', dx:0, dy:0},
  TW:{name:'台湾', short:'台', label:'台湾', dx:0, dy:0},
  HK:{name:'香港', short:'港', label:'香港', dx:20, dy:10},
  MO:{name:'澳门', short:'澳', label:'澳门', dx:-16, dy:12}
};

// 14 个“菜系家族”——同一家族在各时期使用同一色相，便于看出传承与分合
DATA.families = {
  A:{name:'齐鲁—鲁菜', core:['SD']},
  B:{name:'中原—豫晋陕', core:['HA','SX','SN']},
  C:{name:'燕赵—京津冀', core:['BJ','TJ','HE']},
  D:{name:'东北', core:['LN','JL','HL']},
  E:{name:'草原—蒙', core:['NM']},
  F:{name:'西域—新疆', core:['XJ']},
  G:{name:'河陇—甘宁青', core:['GS','NX','QH']},
  H:{name:'青藏—藏', core:['XZ']},
  I:{name:'巴蜀—川渝', core:['SC','CQ']},
  J:{name:'滇黔—西南', core:['YN','GZ']},
  K:{name:'荆楚—湘鄂赣', core:['HB','HN','JX']},
  L:{name:'吴越江南—苏浙沪皖', core:['JS','ZJ','SH','AH']},
  M:{name:'闽—闽台', core:['FJ','TW']},
  N:{name:'岭南—粤桂琼港澳', core:['GD','GX','HI','HK','MO']}
};

// 口味主调
DATA.tastes = {
  xian:{name:'咸鲜·酱香', desc:'盐、酱、豉、酱油带来的发酵咸鲜，黄河流域与京鲁的底色'},
  tian:{name:'鲜甜', desc:'糖与蜜入菜，甜与鲜并举，江南与闽台的标志'},
  suan:{name:'酸香', desc:'醋、酸菜、酸汤、梅子等发酵与果酸主导'},
  xinxiang:{name:'辛香（椒·姜·茱萸）', desc:'辣椒到来之前的“辣”：花椒、姜、茱萸、葱蒜'},
  mala:{name:'麻辣', desc:'辣椒与花椒相遇后的川渝复合味'},
  la:{name:'香辣·酸辣（辣椒）', desc:'辣椒为主的辣味带：湘、黔、赣、桂、滇等'},
  qing:{name:'清鲜·本味', desc:'轻调味、重食材本味与汤鲜，粤闽浙琼台的审美'},
  nai:{name:'奶膻·肉香', desc:'牧区与高原：羊肉、牛肉、奶酪、酥油、孜然'}
};

// 主食
DATA.staples = {
  su:{name:'粟黍（小米·黄米）', desc:'华北最古老的主粮，汉唐以后逐渐让位于麦'},
  mai:{name:'麦（面食）', desc:'石磨普及后北方的主食：饼、面、馒头、馕'},
  dao:{name:'稻（米饭）', desc:'长江流域及以南的主食，宋以后占城稻推动双季稻'},
  daomai:{name:'稻麦兼作', desc:'江淮、汉水与淮河流域的过渡带'},
  qingke:{name:'青稞', desc:'青藏高原的耐寒大麦，糌粑的原料'},
  rou:{name:'肉奶·渔猎', desc:'草原与林海：肉、乳、鱼为主，谷物为辅'},
  shu:{name:'玉米·薯类·杂粮', desc:'明清美洲作物落户山区后的新主食，东北曾以高粱杂粮为主'}
};
