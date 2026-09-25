DATA.periods.push({
  id:'st', name:'隋唐五代', years:'581—960', sub:'隋 · 唐 · 五代十国',
  summary:'大运河贯通南北，长安、洛阳、扬州、广州成为国际都会，“胡食”成为时尚，茶成为国饮，蔗糖工艺从印度引进；宫廷盛宴（烧尾宴）与市井食肆并盛，“南食”“北食”的分野被清楚地记录下来。',
  dims:{
    food:[
      {h:'胡食风尚', t:'胡饼、毕罗、羊肉、葡萄酒风靡长安，“贵人御馔，尽供胡食”。', src:'《旧唐书·舆服志》'},
      {h:'蔗糖引进', t:'唐太宗遣使赴摩揭陀学熬糖法（贞观二十一年，647年），中国从此有了成规模的沙糖生产。', src:'《新唐书·西域传》'},
      {h:'菠菜与西瓜', t:'菠菜（波棱菜）自尼泊尔传入；西瓜稍后于五代由回纥传入中原。', src:'《唐会要》《新五代史·四夷附录》'},
      {h:'茶经', t:'陆羽《茶经》（约760—780年）确立煎茶法，茶成为南北通饮，“茶马互市”开始。', src:'陆羽《茶经》'},
      {h:'海上香料', t:'广州蕃坊聚居阿拉伯、波斯商人，胡椒、丁香、乳香与海产贸易兴盛。', src:'《唐国史补》'}
    ],
    tool:[
      {h:'南青北白', t:'瓷器全面取代漆器：邢窑白瓷“类银类雪”，越窑青瓷“类玉类冰”。', src:'陆羽《茶经·四之器》'},
      {h:'围桌而坐', t:'高足桌椅逐渐流行，晚唐至五代，合食制开始取代一人一案的分餐制。', src:'唐墓壁画宴饮图、《韩熙载夜宴图》'},
      {h:'茶具二十四器', t:'陆羽列风炉、釜、碾、罗等成套茶具，饮茶成为器物系统。', src:'陆羽《茶经》'},
      {h:'石炭与铁锅', t:'北方城市开始用煤（“石炭”），铁锅铸造增多，为宋代炒菜的爆发准备燃料与器具。', src:'《酉阳杂俎》'}
    ],
    tech:[
      {h:'烧尾宴', t:'韦巨源献给唐中宗的烧尾宴留下58道菜名，涵盖蒸、煮、烤、炸、酿、脍、羹，如“光明虾炙”“金铃炙”“御黄王母饭”。', src:'韦巨源《烧尾宴食单》（709年），见《清异录》'},
      {h:'鱼脍鼎盛', t:'唐人食生鱼片风气冠绝历代，“斫脍”名手众多，配以橙、蒜、盐调成的“金齑”。', src:'《砍脍书》（佚，见《酉阳杂俎》）'},
      {h:'冷淘与牢丸', t:'过水凉面（槐叶冷淘）与“汤中牢丸”（水饺汤圆类）见于诗文。', src:'杜甫《槐叶冷淘》'},
      {h:'馕坑式烤炉', t:'蒸饼、胡饼、饆饠的炉烤技术随胡食流行。', src:'唐代西域出土面食'}
    ],
    taste:[
      {h:'尚羊尚胡', t:'长安贵羊肉、贵胡食；胡椒昂贵到成为财富象征——宰相元载抄家时有胡椒八百石。', src:'《新唐书·元载传》'},
      {h:'甜味升级', t:'沙糖与蜂蜜并用，“糖霜”“蜜煎”出现。', src:'《千金要方》'},
      {h:'南食北食', t:'“南食”重鱼鲜、稻米，“北食”重面食、羊肉与酪，分野被记录。', src:'《南部新书》'}
    ]
  },
  regions:[
    {id:'liangjing', fam:'B', name:'两京·关中河洛', provs:['SN','HA'], taste:'xian', staple:'mai', note:'长安与洛阳，胡食风尚的中心，烧尾宴与宫廷菜在此登场。'},
    {id:'hebei', fam:'C', name:'河北·河东', provs:['HE','SX','BJ','TJ'], taste:'xian', staple:'mai', note:'河朔藩镇，面食与酱，胡汉杂处。'},
    {id:'qilu', fam:'A', name:'齐鲁', provs:['SD'], taste:'xian', staple:'mai', note:'面食、海味、盐场；登州港通新罗、日本。'},
    {id:'longyou', fam:'G', name:'陇右·河西', provs:['GS','NX'], taste:'nai', staple:'mai', note:'丝路走廊，胡食与茶马互市；安史之乱后一度为吐蕃所据。'},
    {id:'tubo', fam:'H', name:'吐蕃', provs:['XZ','QH'], taste:'nai', staple:'qingke', note:'青稞、牦牛、酥油茶；文成公主入藏（641年）后茶入吐蕃。'},
    {id:'xiyu', fam:'F', name:'安西·西域', provs:['XJ'], taste:'nai', staple:'mai', note:'高昌、龟兹，馕与葡萄酒；吐鲁番出土唐代饺子、馄饨实物。'},
    {id:'huihe', fam:'E', name:'突厥·回纥', provs:['NM'], taste:'nai', staple:'rou', note:'草原游牧，与唐互市马匹换茶绢。'},
    {id:'jianghuai', fam:'L', name:'江淮·扬州', provs:['JS','SH','AH'], taste:'qing', staple:'daomai', note:'“扬一益二”，运河枢纽，盐、糖、海鲜，淮扬风味的雏形。'},
    {id:'liangzhe', fam:'L', name:'两浙', provs:['ZJ'], taste:'qing', staple:'dao', note:'越窑青瓷，顾渚紫笋贡茶，鱼米之乡。'},
    {id:'jingchu', fam:'K', name:'荆楚·江西', provs:['HB','HN','JX'], taste:'qing', staple:'dao', note:'稻作扩张，茶产区，鱼米。'},
    {id:'jiannan', fam:'I', name:'剑南·巴蜀', provs:['SC','CQ'], taste:'xinxiang', staple:'dao', note:'“扬一益二”的益州，饮食奢华，蒙顶茶与蜀椒；前后蜀宫廷菜。'},
    {id:'min', fam:'M', name:'闽', provs:['FJ'], taste:'qing', staple:'dao', note:'五代闽国，福州、泉州港崛起，海产与佛教素食。'},
    {id:'lingnan', fam:'N', name:'岭南·广州', provs:['GD','GX','HI','HK','MO'], taste:'qing', staple:'dao', note:'蕃坊与香料；刘恂《岭表录异》记岭南异味：蛇、蛤、蚝、槟榔。'},
    {id:'nanzhao', fam:'J', name:'南诏', provs:['YN','GZ'], taste:'suan', staple:'dao', note:'大理地区，稻、茶（普洱茶的先声）。'},
    {id:'bohai', fam:'D', name:'渤海·契丹', provs:['LN','JL','HL'], taste:'xian', staple:'su', note:'渤海国“海东盛国”，粟、豆、渔猎；契丹兴起。'},
    {id:'taiwan', fam:'M', name:'流求', provs:['TW'], taste:'qing', staple:'su', note:'隋书称流求。'}
  ]
});

DATA.periods.push({
  id:'song', name:'两宋', years:'960—1279', sub:'北宋 · 南宋（辽 · 西夏 · 金）',
  summary:'宋代是中国饮食的“近代化”时刻：煤炭与铁锅普及，“炒”成为主流技法；占城稻推广、豆腐与蔗糖普及；汴京、临安的夜市与食店按“南食”“北食”“川饭”分帮经营，地方风味的商业分化第一次被清楚地写进书里。',
  dims:{
    food:[
      {h:'占城稻', t:'1012年宋真宗自福建取占城稻种三万斛推广到江淮两浙，早熟耐旱，双季稻扩大，南方人口与稻米产量激增。', src:'《宋史·食货志》'},
      {h:'豆腐普及', t:'豆腐有“小宰羊”之称，苏轼等文人诗中常见；素菜仿荤（面筋、豆制品）成熟。', src:'陶谷《清异录》'},
      {h:'糖霜谱', t:'王灼《糖霜谱》（1154年）专记遂宁糖霜；蜜饯、糖水成为市井小食。', src:'王灼《糖霜谱》'},
      {h:'羊贵猪贱', t:'北宋宫廷“御厨止用羊肉”，猪肉为平民之食；南宋临安鱼虾海鲜大盛。', src:'《宋会要辑稿》《梦粱录》'},
      {h:'点茶', t:'从煎茶转向点茶，建州北苑龙团凤饼贡茶。', src:'蔡襄《茶录》、赵佶《大观茶论》'}
    ],
    tool:[
      {h:'铁锅+石炭', t:'汴京“数百万家，尽仰石炭，无一家燃薪者”，猛火与铁锅结合，炒法大兴。', src:'庄绰《鸡肋编》'},
      {h:'合食制定型', t:'高桌高椅普及，围桌共食成为常态。', src:'宋代绘画《清明上河图》'},
      {h:'五大名窑', t:'汝、官、哥、钧、定与景德镇青白瓷，成套餐具供应酒楼与家庭。', src:'宋瓷考古'},
      {h:'食店分帮', t:'《东京梦华录》记汴京有“川饭店”“南食店”，并分“北食”“南食”名店，另有专营羹、饼、素食的店铺，正店七十二家，并有外卖。', src:'孟元老《东京梦华录》（序作于1147年）'}
    ],
    tech:[
      {h:'炒爆熘煎炸', t:'技法名目成型，《山家清供》《中馈录》等食谱记录家常做法。', src:'林洪《山家清供》、浦江吴氏《中馈录》'},
      {h:'涮：拨霞供', t:'林洪记武夷山涮兔肉，是火锅涮食的早期明确记载。', src:'《山家清供》“拨霞供”'},
      {h:'面食开花', t:'汤饼、馄饨、包子、馒头、角子（饺子）与冷淘，临安面店“各色面”上百种。', src:'吴自牧《梦粱录》'},
      {h:'腌腊糟醉', t:'金华火腿、糟鱼、醉蟹等江南名产在南宋已具规模。', src:'《梦粱录》《武林旧事》'}
    ],
    taste:[
      {h:'北甜南咸', t:'“大抵南人嗜咸，北人嗜甘，鱼蟹加糖蜜，盖便于北俗也”——沈括记录了与今日相反的甜咸地理。', src:'沈括《梦溪笔谈》卷二十四'},
      {h:'川饭辛香', t:'以花椒、姜、茱萸为“三香”，汴京川饭店的辛香独树一帜——这是没有辣椒的川味。', src:'《东京梦华录》'},
      {h:'酱油与清鲜', t:'“酱油”一词见于《山家清供》，开始取代豉汁；临安的海鲜河鲜与清汤奠定后世“清鲜”审美。', src:'《山家清供》'}
    ]
  },
  regions:[
    {id:'beishi', fam:'B', name:'北食·中原河北', provs:['HA','HE','SX','BJ','TJ'], taste:'tian', staple:'mai', note:'汴京所在，羊肉面食、口味偏甜；北宋后期入金，饮食延续。北京、天津时属辽南京道，后为金中都。'},
    {id:'qilu', fam:'A', name:'齐鲁', provs:['SD'], taste:'xian', staple:'mai', note:'北食一系，面食、海味与酱。'},
    {id:'guanzhong', fam:'B', name:'关中', provs:['SN'], taste:'xian', staple:'mai', note:'羊肉面食，与西夏对峙的前线。'},
    {id:'xixia', fam:'G', name:'西夏·河陇', provs:['GS','NX'], taste:'nai', staple:'mai', note:'党项人的西夏：麦、羊、奶。'},
    {id:'tubo', fam:'H', name:'吐蕃诸部', provs:['QH','XZ'], taste:'nai', staple:'qingke', note:'唃厮啰等部，茶马贸易更盛。'},
    {id:'nanshi', fam:'L', name:'南食·两浙江淮', provs:['JS','ZJ','SH','AH'], taste:'xian', staple:'dao', note:'临安、平江、扬州：鱼鲜蟹醉、糖蜜点心、素菜与面食，宋代餐饮业最繁盛处；“南人嗜咸”。'},
    {id:'chuanfan', fam:'I', name:'川饭·巴蜀', provs:['SC','CQ'], taste:'xinxiang', staple:'dao', note:'汴京“川饭店”的家乡，花椒、姜、茱萸的辛香。'},
    {id:'jinghu', fam:'K', name:'荆湖·江西', provs:['HB','HN','JX'], taste:'xian', staple:'dao', note:'稻米大宗；江西景德镇瓷器与茶叶。'},
    {id:'fujian', fam:'M', name:'福建·建州', provs:['FJ'], taste:'qing', staple:'dao', note:'北苑贡茶、荔枝（蔡襄《荔枝谱》，1059年）、泉州港香料贸易。'},
    {id:'lingnan', fam:'N', name:'岭南', provs:['GD','GX','HI','HK','MO'], taste:'qing', staple:'dao', note:'广州市舶司，海味与糖；周去非《岭外代答》（1178年）记岭南饮食。'},
    {id:'dali', fam:'J', name:'大理', provs:['YN','GZ'], taste:'suan', staple:'dao', note:'大理国，稻作与畜牧，茶马古道。'},
    {id:'liaojin', fam:'D', name:'辽金·东北', provs:['LN','JL','HL'], taste:'nai', staple:'rou', note:'契丹、女真：肉食、乳酪、渔猎与“冻梨”“炙肉”；金朝汉化后面食与酱并行。'},
    {id:'caoyuan', fam:'E', name:'辽·草原', provs:['NM'], taste:'nai', staple:'rou', note:'契丹游牧，“捺钵”四时渔猎。'},
    {id:'xiyu', fam:'F', name:'回鹘·喀喇汗', provs:['XJ'], taste:'nai', staple:'mai', note:'高昌回鹘与喀喇汗王朝，馕与抓饭的前身。'},
    {id:'taiwan', fam:'M', name:'流求·澎湖', provs:['TW'], taste:'qing', staple:'su', note:'南宋时澎湖已隶属泉州晋江县。'}
  ]
});

DATA.periods.push({
  id:'yuan', name:'元', years:'1271—1368', sub:'蒙古 · 大元',
  summary:'蒙古帝国把草原饮食与西域清真饮食带进中原：羊肉、奶食、烤炙成为宫廷主流，回回饮食随色目人扎根西北与云南，蒸馏烧酒兴起。《饮膳正要》是第一部宫廷营养食谱。',
  dims:{
    food:[
      {h:'羊与奶酪', t:'宫廷“诈马宴”整羊烤炙；日常“秃秃麻食”（面片）、“搠罗脱因”等蒙古—回回食品见于食谱。', src:'忽思慧《饮膳正要》（1330年）'},
      {h:'回回食材', t:'回回豆（鹰嘴豆）、回回葱、咱夫兰（藏红花）、马思答吉（乳香）；清真饮食成型，回族在元代形成。', src:'《饮膳正要》《回回药方》'},
      {h:'胡萝卜', t:'“胡萝卜”之名见于元代，西瓜广泛种植。', src:'《饮膳正要》《王祯农书》'},
      {h:'烧酒', t:'李时珍称“烧酒非古法也，自元时始创其法”；元代蒸馏酒（阿剌吉）确已流行。', src:'《本草纲目·谷部》'}
    ],
    tool:[
      {h:'蒸馏器', t:'“阿剌吉”蒸馏器传入，白酒工艺的起点之一。', src:'《饮膳正要》《居家必用事类全集》'},
      {h:'三种饭馆', t:'大都的汉、蒙、回三种饮食并存，饭馆按族群分设。', src:'《析津志》'},
      {h:'王祯农书', t:'系统记录水磨、水碾等农产加工机械。', src:'王祯《农书》（1313年）'}
    ],
    tech:[
      {h:'烤全羊', t:'烤炙与整只烹饪：烤全羊、炙肉、羊肚等草原技法进入宫廷。', src:'《饮膳正要》'},
      {h:'秃秃麻食', t:'蒙古面片与回回“卷煎饼”，面食技法进一步与中亚交流。', src:'《饮膳正要》《居家必用事类全集》'},
      {h:'食疗体系', t:'《饮膳正要》首次以“食疗”“食补”体系统合烹饪，养生饮食观念官方化。', src:'《饮膳正要》'}
    ],
    taste:[
      {h:'肉膻奶香', t:'成为北方上层主调；清真的咸香与孜然、胡椒、藏红花等香料进入西北与云南。', src:'—'},
      {h:'江南延续', t:'甜、鲜、糟醉；倪瓒《云林堂饮食制度集》记录苏南文人精致菜。', src:'倪瓒《云林堂饮食制度集》'}
    ]
  },
  regions:[
    {id:'dadu', fam:'C', name:'大都·燕京', provs:['BJ','TJ','HE'], taste:'nai', staple:'mai', note:'元大都，蒙、汉、回三种饮食并存，宫廷羊肉与奶食。'},
    {id:'zhongyuan', fam:'B', name:'腹里·中原', provs:['HA','SX'], taste:'xian', staple:'mai', note:'中书省直辖“腹里”，面食与酱豉延续。'},
    {id:'qilu', fam:'A', name:'齐鲁', provs:['SD'], taste:'xian', staple:'mai', note:'属腹里，海盐与面食。'},
    {id:'caoyuan', fam:'E', name:'岭北·草原', provs:['NM'], taste:'nai', staple:'rou', note:'蒙古本部，肉乳为主。'},
    {id:'xibei', fam:'G', name:'陕西·甘肃行省', provs:['SN','GS','NX'], taste:'xian', staple:'mai', note:'回回聚居，清真饮食形成（牛羊肉、面食）。'},
    {id:'xiyu', fam:'F', name:'察合台·西域', provs:['XJ'], taste:'nai', staple:'mai', note:'察合台汗国，馕与烤肉。'},
    {id:'tubo', fam:'H', name:'宣政院辖地', provs:['XZ','QH'], taste:'nai', staple:'qingke', note:'元设宣政院；酥油茶、糌粑。'},
    {id:'jiangzhe', fam:'L', name:'江浙行省', provs:['JS','ZJ','SH','AH'], taste:'qing', staple:'dao', note:'宋风延续，倪瓒等文人菜；安徽南部属江浙行省。'},
    {id:'fujian', fam:'M', name:'福建·泉州', provs:['FJ'], taste:'qing', staple:'dao', note:'泉州为元代最大港口之一，海外香料与蕃商饮食。'},
    {id:'huguang', fam:'K', name:'湖广·江西行省', provs:['HB','HN','JX'], taste:'xian', staple:'dao', note:'稻米大宗。'},
    {id:'sichuan', fam:'I', name:'四川行省', provs:['SC','CQ'], taste:'xinxiang', staple:'dao', note:'宋元战争后人口锐减，饮食传统受挫，等待明清移民重建。'},
    {id:'yunnan', fam:'J', name:'云南行省', provs:['YN','GZ'], taste:'suan', staple:'dao', note:'赛典赤治滇，回族与汉人移民带来清真与中原饮食。'},
    {id:'lingnan', fam:'N', name:'岭南', provs:['GD','GX','HI','HK','MO'], taste:'qing', staple:'dao', note:'广东属江西行省，广西属湖广行省；广州港延续海贸。'},
    {id:'liaoyang', fam:'D', name:'辽阳行省', provs:['LN','JL','HL'], taste:'xian', staple:'su', note:'女真、汉人，渔猎与粟豆。'},
    {id:'taiwan', fam:'M', name:'澎湖巡检司', provs:['TW'], taste:'qing', staple:'su', note:'元代设澎湖巡检司。'}
  ]
});
