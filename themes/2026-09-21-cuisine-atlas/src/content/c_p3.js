DATA.periods.push({
  id:'ming', name:'明', years:'1368—1644', sub:'大明',
  summary:'美洲作物经海路登陆——辣椒、玉米、番薯、马铃薯、花生、南瓜、番茄——这是中国餐桌的“新大陆时刻”，但辣椒此时还是观赏花卉。江南富庶带来甜、精、雅的文人饮食，徽商、晋商、盐商让菜随商走，“菜系”的地理格局开始成型。',
  dims:{
    food:[
      {h:'辣椒登陆', t:'目前所见最早的记载是高濂《遵生八笺》（1591年刊行，“番椒”条见于稍后的翻刻修订本）：“番椒丛生白花，子俨秃笔头，味辣色红，甚可观”——作为观赏植物。', src:'高濂《遵生八笺·燕闲清赏笺》'},
      {h:'番薯玉米', t:'1593年陈振龙从吕宋携薯藤回福建；玉米约16世纪中叶传入（《平凉府志》1560年记“番麦”）；花生（《常熟县志》1503年）、马铃薯、南瓜、番茄（“番柿”，观赏）陆续登陆。', src:'《金薯传习录》《平凉府志》《群芳谱》'},
      {h:'白糖工艺', t:'《天工开物》（1637年）记“黄泥水淋法”制白糖，福建、广东成为糖业中心，糖价下降。', src:'宋应星《天工开物·甘嗜》'},
      {h:'猪肉上位', t:'明代猪肉取代羊肉成为汉地主要肉食。', src:'《本草纲目·兽部》'},
      {h:'胡椒折俸', t:'郑和下西洋带回大量胡椒，一度用作官俸发放。', src:'《明史·食货志》'}
    ],
    tool:[
      {h:'佛山铁锅', t:'“广锅”行销全国甚至海外，铸铁锅质量与产量空前。', src:'《天工开物·冶铸》'},
      {h:'紫砂与散茶', t:'朱元璋罢团茶（1391年）后散茶冲泡成为主流，宜兴紫砂壶随之兴起。', src:'《明会典》、周高起《阳羡茗壶系》'},
      {h:'青花餐具', t:'景德镇青花成套餐具走进富户，八仙桌、圆桌合食制完全定型。', src:'明代景德镇窑址'},
      {h:'锅台风箱', t:'多火眼大灶、风箱与“锅台”成为北方民居标准。', src:'《天工开物》'}
    ],
    tech:[
      {h:'术语系统化', t:'炒、爆、熘、煎、炸、烹、烧、焖、炖、煨、蒸、烩、烤、涮、卤、酱、腌、糟、醉等技法名目基本齐备。', src:'宋诩《宋氏养生部》（1504年）、《易牙遗意》'},
      {h:'食谱专业化', t:'《宋氏养生部》《遵生八笺》《竹屿山房杂部》记录数百道菜的具体做法。', src:'同上'},
      {h:'地方技法定型', t:'徽州臭鳜鱼、江南糟醉、山东爆炒、福建红糟等地方技法定型。', src:'—'},
      {h:'御膳鲁厨', t:'光禄寺、尚膳监规模化，宫廷菜以山东厨师为主力，鲁菜进入宫廷。', src:'《明宫史》'}
    ],
    taste:[
      {h:'南甜北咸', t:'江南糖价下降、富庶精致，“甜”成为苏杭标志；北方以酱、盐为主——甜咸地理与宋代倒转。', src:'《遵生八笺》《宋氏养生部》'},
      {h:'辣椒仍在门外', t:'明人吃辣靠花椒、姜、茱萸、胡椒、芥末。', src:'—'},
      {h:'菜随商走', t:'徽商与晋商把家乡口味带到扬州、北京，商帮饮食成为“菜系”流动的推手。', src:'《扬州画舫录》追述'}
    ]
  },
  regions:[
    {id:'jingshi', fam:'C', name:'京师·北直隶', provs:['BJ','TJ','HE'], taste:'xian', staple:'mai', note:'永乐迁都后，宫廷与官府菜集中；南京传来的片皮鸭落户北京（便宜坊传承自1416年）。'},
    {id:'shandong', fam:'A', name:'山东', provs:['SD'], taste:'xian', staple:'mai', note:'鲁菜雏形：胶东海鲜与济南菜，爆、扒、汤，进入宫廷。'},
    {id:'zhongyuan', fam:'B', name:'河南·山西·陕西', provs:['HA','SX','SN'], taste:'xian', staple:'mai', note:'面食王国，晋商、陕商；山西醋，河南“扒”“烧”。'},
    {id:'xibei', fam:'G', name:'甘肃·宁夏·青海', provs:['GS','NX','QH'], taste:'xian', staple:'mai', note:'河西走廊，回族清真牛羊面食。'},
    {id:'jiangnan', fam:'L', name:'江南·苏松杭', provs:['JS','ZJ','SH'], taste:'tian', staple:'dao', note:'甜、鲜、精，文人饮食（高濂是杭州人），苏帮菜、杭帮菜成型。'},
    {id:'huizhou', fam:'L', name:'徽州·安徽', provs:['AH'], taste:'xian', staple:'daomai', note:'徽商崛起，徽菜随商路传播，重油重色、火腿与臭鳜鱼。'},
    {id:'huguang', fam:'K', name:'湖广·江西', provs:['HB','HN','JX'], taste:'suan', staple:'dao', note:'“湖广熟，天下足”，稻作中心；江西瓷都景德镇。'},
    {id:'sichuan', fam:'I', name:'四川', provs:['SC','CQ'], taste:'xinxiang', staple:'dao', note:'明初移民（“湖广填四川”第一波），饮食重建。'},
    {id:'fujian', fam:'M', name:'福建', provs:['FJ'], taste:'qing', staple:'dao', note:'番薯登陆（1593年），闽菜、红糟，海禁与走私并存的海洋饮食。'},
    {id:'lingnan', fam:'N', name:'广东·广西', provs:['GD','GX','HI','HK','MO'], taste:'qing', staple:'dao', note:'澳门开埠（1557年），美洲作物与番茄、辣椒的海路入口；广州糖业。'},
    {id:'yungui', fam:'J', name:'云南·贵州', provs:['YN','GZ'], taste:'suan', staple:'dao', note:'明代大规模屯军移民，贵州建省（1413年）；玉米、辣椒后来在此扎根。'},
    {id:'wusizang', fam:'H', name:'乌思藏', provs:['XZ'], taste:'nai', staple:'qingke', note:'酥油茶、糌粑。'},
    {id:'xiyu', fam:'F', name:'叶尔羌·吐鲁番', provs:['XJ'], taste:'nai', staple:'mai', note:'馕、抓饭、葡萄干。'},
    {id:'menggu', fam:'E', name:'蒙古', provs:['NM'], taste:'nai', staple:'rou', note:'蒙古诸部，肉乳为主。'},
    {id:'dongbei', fam:'D', name:'辽东·女真', provs:['LN','JL','HL'], taste:'xian', staple:'su', note:'辽东都司汉人农耕，女真渔猎，粟、豆、猪。'},
    {id:'taiwan', fam:'M', name:'台湾', provs:['TW'], taste:'qing', staple:'dao', note:'明末荷兰、西班牙据台，闽南移民开始，稻蔗种植。'}
  ],
  overrides:{ SX:{taste:'suan'} }
});

DATA.periods.push({
  id:'qing', name:'清', years:'1644—1912', sub:'大清',
  summary:'辣椒从观赏走上餐桌，先在贵州“代盐”，再席卷湖南、四川，酸辣、香辣、麻辣的现代辣味格局在乾隆至光绪年间定型；满汉全席集大成，袁枚《随园食单》把饮食写成美学；清末民初，京师、山东、四川、广东、福建、江宁、苏州、扬州等“各省特色肴馔”已成常识，为后来的“菜系”划分打下基础。',
  dims:{
    food:[
      {h:'辣椒上桌', t:'康熙《思州府志》（约1721年编成、1722年刻本）记贵州“海椒，俗名辣火，土苗用以代盐”，是现存最早的食用辣椒记录；乾隆年间湘、黔普遍食辣，四川方志最早见于乾隆十四年（1749年）《大邑县志》“秦椒，又名海椒”，嘉庆年间种植食用迅速扩展，同治年间“山野遍种”，光绪以后川人“每饭每菜，非辣不可”。', src:'《思州府志》《大邑县志》、徐心余《蜀游闻见录》'},
      {h:'人口与薯麦', t:'番薯、玉米、马铃薯在山区大规模推广，支撑清代人口从1亿到4亿的增长；番茄晚清才开始食用。', src:'何炳棣《美洲作物的引进、传播及其对中国粮食生产的影响》'},
      {h:'山珍海味', t:'燕窝、鱼翅、海参、鲍鱼成为宴席等级标志，“海参席”“燕窝席”见于食单。', src:'《随园食单》《调鼎集》'},
      {h:'调味品牌', t:'蚝油（李锦记，1888年）、六必居酱菜、郫县豆瓣、镇江香醋等地方调味品牌化。', src:'—'},
      {h:'京师烤鸭', t:'便宜坊焖炉与全聚德（1864年）挂炉烤鸭。', src:'—'}
    ],
    tool:[
      {h:'火锅', t:'清宫火锅盛行，嘉庆元年千叟宴（1796年）动用火锅一千五百余只；北方铜锅涮肉、川渝铁锅麻辣火锅（清末重庆码头）起源。', src:'清宫御膳档案'},
      {h:'砂锅汽锅', t:'砂锅、汽锅（云南建水）、瓦罐（江西）、蒸笼（粤式点心）等器具与地方菜互相塑造。', src:'—'},
      {h:'炒锅分化', t:'北方双耳生铁锅、南方单柄薄锅，广式“镬”配猛火灶讲究“镬气”。', src:'—'},
      {h:'餐馆业成熟', t:'北京“八大楼”“八大居”，扬州盐商家厨，广州茶楼“一盅两件”。', src:'《扬州画舫录》《清稗类钞》'}
    ],
    tech:[
      {h:'满汉全席', t:'满洲烧烤与汉族名菜合一，宴席程式化。', src:'李斗《扬州画舫录》（1795年）'},
      {h:'随园食单', t:'袁枚提出“须知单”“戒单”，讲火候、配搭、本味，是中国饮食美学的经典。', src:'袁枚《随园食单》（1792年）'},
      {h:'吊汤', t:'鲁菜清汤奶汤、淮扬清炖、粤菜上汤——“唱戏的腔，厨子的汤”。', src:'—'},
      {h:'复合味定型', t:'川菜麻辣、鱼香、怪味、家常等味型在清末民初成形，“一菜一格，百菜百味”。', src:'—'}
    ],
    taste:[
      {h:'辣椒走廊', t:'黔（酸辣）、湘（香辣）、川渝（麻辣）、赣鄂（辣）形成辣味带；粤、江南、京鲁基本不辣。', src:'蓝勇《中国饮食辛辣口味的地理分布及其成因研究》'},
      {h:'各省特色肴馔', t:'咸鲜（鲁、京）、鲜甜（苏、锡、杭、沪）、清鲜（粤、闽）、麻辣（川）四大风味区成形；徐珂总结“肴馔之有特色者，为京师、山东、四川、广东、福建、江宁、苏州、镇江、扬州、淮安”——“菜系”这个词本身要到20世纪50—70年代才出现。', src:'徐珂《清稗类钞·饮食类》（1916年）'},
      {h:'南甜北咸', t:'甜咸地理最终倒转为“南甜北咸”，与宋代记载相反。', src:'—'}
    ]
  },
  regions:[
    {id:'jingshi', fam:'C', name:'京师·直隶', provs:['BJ','TJ','HE'], taste:'xian', staple:'mai', note:'满汉全席、烤鸭、涮羊肉、宫廷与官府菜，鲁菜厨师为骨干；天津码头菜“八大碗”。'},
    {id:'lu', fam:'A', name:'鲁', provs:['SD'], taste:'xian', staple:'mai', note:'鲁菜成熟：济南（爆、汤）与胶东（海鲜）两大流派，是宫廷菜与京菜的母本；闯关东把鲁菜带到东北。'},
    {id:'yujinshaan', fam:'B', name:'豫·晋·陕', provs:['HA','SX','SN'], taste:'xian', staple:'mai', note:'面食核心区；山西陈醋、陕西羊肉泡馍、河南烩面的前身。'},
    {id:'xibei', fam:'G', name:'甘·宁·青', provs:['GS','NX','QH'], taste:'xian', staple:'mai', note:'清真牛羊面食；兰州牛肉面据传起于清末民初。'},
    {id:'huaiyang', fam:'L', name:'苏·淮扬', provs:['JS','SH'], taste:'tian', staple:'dao', note:'扬州盐商菜、苏州船菜，刀工与火候，随园所在的江宁也在此；上海开埠（1843年）后本帮菜萌芽。'},
    {id:'zhe', fam:'L', name:'浙', provs:['ZJ'], taste:'qing', staple:'dao', note:'杭帮、宁波、绍兴三路，鱼鲜、糟醉、黄酒。'},
    {id:'hui', fam:'L', name:'徽', provs:['AH'], taste:'xian', staple:'daomai', note:'徽商鼎盛，徽菜在扬州、汉口、上海开馆；重油、重色、重火功。'},
    {id:'min', fam:'M', name:'闽', provs:['FJ'], taste:'qing', staple:'dao', note:'闽菜（福州佛跳墙、闽南沙茶）、红糟、海味；下南洋带回沙茶等南洋风味。'},
    {id:'yue', fam:'N', name:'粤', provs:['GD','HK','MO'], taste:'qing', staple:'dao', note:'一口通商（1757—1842年）、十三行，粤菜融合海味、野味与西式技法；茶楼点心；香港（1842年）、澳门成为中西饮食交汇处。'},
    {id:'gui', fam:'N', name:'桂', provs:['GX'], taste:'la', staple:'dao', note:'桂北酸辣、桂南清淡，米粉。'},
    {id:'qiong', fam:'N', name:'琼', provs:['HI'], taste:'qing', staple:'dao', note:'海南四大名菜（文昌鸡等）雏形，椰、海鲜。'},
    {id:'xiang', fam:'K', name:'湘', provs:['HN'], taste:'la', staple:'dao', note:'辣椒普及，湘菜香辣、腊味、酸；湘军将领把湘菜带到各地。'},
    {id:'chuan', fam:'I', name:'川·渝', provs:['SC','CQ'], taste:'mala', staple:'dao', note:'“湖广填四川”后饮食重建；辣椒乾隆年间见于方志，嘉庆以后与花椒相遇，麻辣川菜在光绪年间（清末）定型；陈麻婆豆腐（1862年）。'},
    {id:'e', fam:'K', name:'鄂', provs:['HB'], taste:'xian', staple:'dao', note:'汉口码头，鱼米之乡，武昌鱼、热干面前身；辣味居中。'},
    {id:'gan', fam:'K', name:'赣', provs:['JX'], taste:'la', staple:'dao', note:'辣椒进入江西，瓦罐汤、赣南客家菜。'},
    {id:'dian', fam:'J', name:'滇', provs:['YN'], taste:'la', staple:'shu', note:'过桥米线、汽锅鸡、宣威火腿、菌子，多民族饮食。'},
    {id:'qian', fam:'J', name:'黔', provs:['GZ'], taste:'la', staple:'shu', note:'最早食辣之地，酸汤、糟辣，苗侗饮食。'},
    {id:'zang', fam:'H', name:'藏', provs:['XZ'], taste:'nai', staple:'qingke', note:'酥油茶、糌粑、牦牛肉。'},
    {id:'xinjiang', fam:'F', name:'新疆', provs:['XJ'], taste:'nai', staple:'mai', note:'1884年建省，馕、抓饭、烤肉，回、汉移民。'},
    {id:'meng', fam:'E', name:'蒙', provs:['NM'], taste:'nai', staple:'rou', note:'蒙古族奶食肉食，晋商“走西口”带来面食与烧麦。'},
    {id:'dongbei', fam:'D', name:'东北', provs:['LN','JL','HL'], taste:'xian', staple:'shu', note:'满族饮食（萨其马、酸菜、白肉血肠）与闯关东的山东、河北移民融合，高粱、大豆。'},
    {id:'tai', fam:'M', name:'台', provs:['TW'], taste:'qing', staple:'dao', note:'1683年后闽粤移民大规模入台，米食、卤肉、担仔面前身；1895年后受日本影响。'}
  ],
  overrides:{ SX:{taste:'suan'} }
});

DATA.periods.push({
  id:'mg', name:'民国', years:'1912—1949', sub:'中华民国',
  summary:'城市化与战争推动地方菜流动：上海成为“海派”融合场，北京“八大楼”“八大居”云集各帮，抗战内迁把川菜带到大后方并反向输出；味精、罐头、西餐进入日常。餐饮业按“帮口”分类——京帮、苏帮、锡帮、宁帮、徽帮、粤帮、川帮——这是“菜系”概念的前身。',
  dims:{
    food:[
      {h:'味精', t:'日本“味の素”1909年上市，吴蕴初1923年在上海创办天厨味精厂，鲜味工业化。', src:'—'},
      {h:'番菜西点', t:'西餐（“番菜”）在上海、天津、哈尔滨流行，面包、咖啡、罐头进入城市；哈尔滨红肠、大列巴受俄侨影响。', src:'—'},
      {h:'洋菜普及', t:'番茄、洋葱、卷心菜等“洋”菜普及，番茄炒蛋成为家常。', src:'—'},
      {h:'战时杂粮', t:'抗战时期粮食统制，杂粮与番薯保障了大后方。', src:'—'}
    ],
    tool:[
      {h:'煤炉洋铁', t:'煤炉、洋铁（马口铁）壶锅、搪瓷器具进入家庭；煤气灶在上海租界出现。', src:'—'},
      {h:'餐馆黄金期', t:'北京八大楼（以鲁菜为主），上海本帮馆（老正兴）、川菜馆，广州“四大酒家”。', src:'—'},
      {h:'冰箱制冰', t:'电冰箱与制冰厂让海鲜与冷饮走得更远。', src:'—'}
    ],
    tech:[
      {h:'川菜定型', t:'成都荣乐园（1912年）等名馆与蓝光鉴等名厨确立“一菜一格，百菜百味”的现代川菜体系。', src:'—'},
      {h:'食在广州', t:'“食在广州”口号（1920年代），点心、烧腊、汤品体系完成，并随华侨走向世界。', src:'—'},
      {h:'海派融合', t:'本帮浓油赤酱吸收苏锡、宁波、粤、川与西餐，形成融合风格。', src:'—'},
      {h:'烹饪写作', t:'现代食谱与烹饪教育萌芽。', src:'—'}
    ],
    taste:[
      {h:'帮口分类', t:'上海餐饮业分京帮、苏帮、锡帮、宁帮、徽帮、粤帮、川帮等“帮口”；“菜系”一词要到1950—60年代才出现，“四大菜系”（鲁、川、粤、淮扬）在1970—80年代才成为通行说法。', src:'民国报刊、《中国菜谱》丛书（1975年起）'},
      {h:'麻辣出川', t:'抗战期间重庆、成都聚集全国人口，战后川菜随人流散到各地。', src:'—'},
      {h:'制造的鲜', t:'味精、酱油厂让“鲜”脱离高汤，成为工业味觉。', src:'—'}
    ]
  },
  regions:[
    {id:'jing', fam:'C', name:'京·津·冀', provs:['BJ','TJ','HE'], taste:'xian', staple:'mai', note:'八大楼、八大居，鲁菜为骨；天津租界西餐与津味小吃。'},
    {id:'lu', fam:'A', name:'鲁', provs:['SD'], taste:'xian', staple:'mai', note:'鲁菜为北方菜系正宗，青岛开埠带来啤酒。'},
    {id:'yujinshaan', fam:'B', name:'豫·晋·陕', provs:['HA','SX','SN'], taste:'xian', staple:'mai', note:'面食核心区。'},
    {id:'xibei', fam:'G', name:'甘·宁·青', provs:['GS','NX','QH'], taste:'xian', staple:'mai', note:'兰州牛肉面（马保子，1915年）成名。'},
    {id:'hu', fam:'L', name:'沪·海派', provs:['SH'], taste:'tian', staple:'dao', note:'本帮浓油赤酱与各帮、西餐融合，“海派”形成。'},
    {id:'su', fam:'L', name:'苏·淮扬', provs:['JS'], taste:'tian', staple:'dao', note:'淮扬菜为“国宴”基底之一。'},
    {id:'zhe', fam:'L', name:'浙', provs:['ZJ'], taste:'qing', staple:'dao', note:'杭帮、甬帮进入上海。'},
    {id:'hui', fam:'L', name:'徽', provs:['AH'], taste:'xian', staple:'daomai', note:'徽菜馆在上海一度多达数百家。'},
    {id:'min', fam:'M', name:'闽', provs:['FJ'], taste:'qing', staple:'dao', note:'闽菜与南洋华侨饮食往来。'},
    {id:'yue', fam:'N', name:'粤·港·澳', provs:['GD','HK','MO'], taste:'qing', staple:'dao', note:'“食在广州”，粤菜随华侨走向世界。'},
    {id:'gui', fam:'N', name:'桂', provs:['GX'], taste:'la', staple:'dao', note:'桂林米粉、南宁老友粉。'},
    {id:'qiong', fam:'N', name:'琼', provs:['HI'], taste:'qing', staple:'dao', note:'海南鸡饭随琼籍华侨传到南洋。'},
    {id:'xiang', fam:'K', name:'湘', provs:['HN'], taste:'la', staple:'dao', note:'湘菜名馆在长沙兴起。'},
    {id:'chuan', fam:'I', name:'川·渝', provs:['SC','CQ'], taste:'mala', staple:'dao', note:'陪都重庆汇聚全国人口，川菜大众化并外传。'},
    {id:'e', fam:'K', name:'鄂', provs:['HB'], taste:'xian', staple:'dao', note:'武汉三镇码头饮食，热干面（1930年代）。'},
    {id:'gan', fam:'K', name:'赣', provs:['JX'], taste:'la', staple:'dao', note:'赣菜香辣。'},
    {id:'dian', fam:'J', name:'滇', provs:['YN'], taste:'la', staple:'shu', note:'抗战时昆明汇聚各地饮食。'},
    {id:'qian', fam:'J', name:'黔', provs:['GZ'], taste:'la', staple:'shu', note:'酸辣黔菜。'},
    {id:'zang', fam:'H', name:'藏', provs:['XZ'], taste:'nai', staple:'qingke', note:'酥油茶、糌粑。'},
    {id:'xinjiang', fam:'F', name:'新疆', provs:['XJ'], taste:'nai', staple:'mai', note:'馕、抓饭、烤肉。'},
    {id:'meng', fam:'E', name:'蒙', provs:['NM'], taste:'nai', staple:'rou', note:'奶食肉食。'},
    {id:'dongbei', fam:'D', name:'东北', provs:['LN','JL','HL'], taste:'xian', staple:'shu', note:'哈尔滨俄式饮食、锅包肉（1900年代）等东北菜定型。'},
    {id:'tai', fam:'M', name:'台', provs:['TW'], taste:'qing', staple:'dao', note:'日据时期日式饮食影响，米食与小吃。'}
  ],
  overrides:{ SX:{taste:'suan'} }
});

DATA.periods.push({
  id:'dd', name:'当代', years:'1949—今', sub:'中华人民共和国',
  summary:'1980年《人民日报》一篇文章让“八大菜系”成为通行说法；改革开放后粤菜北上、川菜全国化、湘菜崛起，火锅与外卖重塑餐桌；东北大米、新疆大盘鸡、兰州拉面、沙县小吃、螺蛳粉这些“新地方味”都是近四十年的产物。菜系仍在演化——今天的中国味觉比历史上任何时候都更“麻辣”，也更“融合”。',
  dims:{
    food:[
      {h:'主食版图重绘', t:'东北由杂粮区变为最大的粳稻产区（朝鲜族移民引入水稻，1950年代后大规模开发北大荒），玉米转为饲料，肉蛋奶消费激增。', src:'—'},
      {h:'调味品工业', t:'鸡精、蚝油、生抽老抽、郫县豆瓣、老干妈（1996年）、火锅底料把地方味标准化并全国流通。', src:'—'},
      {h:'冷链与反季', t:'反季节蔬菜与冷链（1990年代起）松动了地理对“时令”的约束，海鲜与热带水果走向内陆。', src:'—'},
      {h:'新食材', t:'西兰花、生菜、牛油果、三文鱼、小龙虾（1990年代盱眙起）等常态化。', src:'—'}
    ],
    tool:[
      {h:'家庭厨房电气化', t:'燃气灶（1980—90年代城市普及）、电饭煲（1980年代引进）、高压锅、电磁炉、微波炉、空气炸锅（2020年前后）。', src:'—'},
      {h:'商用与中央厨房', t:'猛火灶、万能蒸烤箱与中央厨房；连锁餐饮（海底捞1994年）与预制菜（2020年代）。', src:'—'},
      {h:'外卖平台', t:'2010年代外卖平台与冷链把“堂食”变成“到家”。', src:'—'}
    ],
    tech:[
      {h:'教育与标准化', t:'1980年代烹饪专业进入职业教育，各菜系技法编成教材；中国烹饪协会1987年成立。', src:'—'},
      {h:'新派与融合', t:'新派川菜、新派粤菜、创意淮扬与融合菜；米其林指南进入上海（2016年）、广州（2018年）、北京（2019年）。', src:'—'},
      {h:'火锅化', t:'麻辣火锅从重庆走向全国（1990年代起），成为最大单一餐饮品类。', src:'—'},
      {h:'小吃连锁化', t:'沙县小吃（1990年代起）、兰州拉面（青海化隆人自1980年代在全国开店）、螺蛳粉（2010年代网红化）。', src:'—'}
    ],
    taste:[
      {h:'麻辣全国化', t:'川湘菜馆遍布南北，辣味从“辣椒走廊”扩散到全国，年轻人口味嗜辣。', src:'—'},
      {h:'南甜北咸东辣西酸', t:'成为民间口诀，但现实是各地口味互相渗透。', src:'—'},
      {h:'鲜甜辣并进', t:'粤菜清鲜（1980—90年代北上）、江浙甜鲜、川湘麻辣三种审美并存；奶茶等“甜饮”成为新味觉。', src:'—'},
      {h:'地方复兴', t:'淮扬、本帮、潮汕、云南、新疆、贵州菜“出圈”，淄博烧烤（2023年）式的城市饮食IP。', src:'—'}
    ]
  },
  regions:[
    {id:'jing', fam:'C', name:'京菜', provs:['BJ'], taste:'xian', staple:'mai', note:'宫廷菜、官府菜（谭家菜）、清真菜与鲁菜四流汇合；烤鸭、涮羊肉、炸酱面。'},
    {id:'jin', fam:'C', name:'津菜', provs:['TJ'], taste:'xian', staple:'mai', note:'河海两鲜，“八大碗”“四大扒”，狗不理、煎饼馃子。'},
    {id:'ji', fam:'C', name:'冀菜', provs:['HE'], taste:'xian', staple:'mai', note:'直隶官府菜、塞外野味、沿海海鲜三派，驴肉火烧。'},
    {id:'lu', fam:'A', name:'鲁菜', provs:['SD'], taste:'xian', staple:'mai', note:'八大菜系之首：济南、胶东、孔府三派；爆、扒、烧、塌与清汤奶汤。'},
    {id:'jinshanxi', fam:'B', name:'晋菜', provs:['SX'], taste:'suan', staple:'mai', note:'面食之乡，老陈醋，过油肉。'},
    {id:'shaan', fam:'B', name:'陕菜', provs:['SN'], taste:'xian', staple:'mai', note:'羊肉泡馍、肉夹馍、凉皮、油泼面。'},
    {id:'yu', fam:'B', name:'豫菜', provs:['HA'], taste:'xian', staple:'mai', note:'烩面、胡辣汤、鲤鱼焙面，“五味调和”。'},
    {id:'long', fam:'G', name:'陇菜', provs:['GS'], taste:'xian', staple:'mai', note:'兰州牛肉面、手抓羊肉、浆水面。'},
    {id:'ning', fam:'G', name:'宁夏菜', provs:['NX'], taste:'xian', staple:'mai', note:'清真手抓、羊杂碎、八宝茶。'},
    {id:'qinghai', fam:'G', name:'青海菜', provs:['QH'], taste:'nai', staple:'mai', note:'手抓、酸奶、尕面片；化隆人把“兰州拉面”开遍全国。'},
    {id:'xinjiang', fam:'F', name:'新疆菜', provs:['XJ'], taste:'nai', staple:'mai', note:'馕、抓饭、烤肉串、大盘鸡（1980年代沙湾）、拉条子。'},
    {id:'meng', fam:'E', name:'蒙餐', provs:['NM'], taste:'nai', staple:'rou', note:'手把肉、烤全羊、奶茶、奶豆腐、烧麦。'},
    {id:'zang', fam:'H', name:'藏餐', provs:['XZ'], taste:'nai', staple:'qingke', note:'糌粑、酥油茶、青稞酒、牦牛肉。'},
    {id:'dongbei', fam:'D', name:'东北菜', provs:['LN','JL','HL'], taste:'xian', staple:'dao', note:'锅包肉、猪肉炖粉条、酸菜白肉、小鸡炖蘑菇、延边冷面；东北大米。'},
    {id:'hu', fam:'L', name:'本帮·海派', provs:['SH'], taste:'tian', staple:'dao', note:'浓油赤酱：红烧肉、生煎、南翔小笼。'},
    {id:'su', fam:'L', name:'苏菜', provs:['JS'], taste:'tian', staple:'dao', note:'淮扬、金陵、苏锡、徐海四派；狮子头、文思豆腐、松鼠鳜鱼。'},
    {id:'zhe', fam:'L', name:'浙菜', provs:['ZJ'], taste:'qing', staple:'dao', note:'杭州、宁波、绍兴、温州；西湖醋鱼、东坡肉、龙井虾仁。'},
    {id:'hui', fam:'L', name:'徽菜', provs:['AH'], taste:'xian', staple:'daomai', note:'臭鳜鱼、毛豆腐、火腿炖甲鱼；重油重色重火功。'},
    {id:'min', fam:'M', name:'闽菜', provs:['FJ'], taste:'qing', staple:'dao', note:'福州、闽南、闽西；佛跳墙、红糟、沙茶、沙县小吃。'},
    {id:'tai', fam:'M', name:'台菜', provs:['TW'], taste:'tian', staple:'dao', note:'闽南底色加眷村各省菜与日式影响；卤肉饭、牛肉面、珍珠奶茶（1980年代）。'},
    {id:'gan', fam:'K', name:'赣菜', provs:['JX'], taste:'la', staple:'dao', note:'瓦罐汤、三杯鸡、莲花血鸭。'},
    {id:'e', fam:'K', name:'鄂菜（楚菜）', provs:['HB'], taste:'xian', staple:'dao', note:'武昌鱼、热干面、排骨藕汤、沔阳三蒸。'},
    {id:'xiang', fam:'K', name:'湘菜', provs:['HN'], taste:'la', staple:'dao', note:'剁椒鱼头、小炒肉、腊味合蒸、口味虾（1990年代长沙）。'},
    {id:'yue', fam:'N', name:'粤菜', provs:['GD'], taste:'qing', staple:'dao', note:'广府、潮汕、客家三派；白切鸡、烧鹅、老火汤、早茶点心、潮汕牛肉火锅。'},
    {id:'hk', fam:'N', name:'港式', provs:['HK'], taste:'qing', staple:'dao', note:'茶餐厅（1950年代起）、烧腊、云吞面、丝袜奶茶。'},
    {id:'mo', fam:'N', name:'澳门菜', provs:['MO'], taste:'qing', staple:'dao', note:'土生葡菜：葡国鸡、非洲鸡、猪扒包、葡挞。'},
    {id:'gui', fam:'N', name:'桂菜', provs:['GX'], taste:'la', staple:'dao', note:'桂林米粉、柳州螺蛳粉、南宁老友粉、柠檬鸭。'},
    {id:'qiong', fam:'N', name:'琼菜', provs:['HI'], taste:'qing', staple:'dao', note:'文昌鸡、加积鸭、东山羊、和乐蟹，海南鸡饭。'},
    {id:'chuan', fam:'I', name:'川菜（川渝）', provs:['SC','CQ'], taste:'mala', staple:'dao', note:'回锅肉、麻婆豆腐、宫保鸡丁、水煮鱼、重庆火锅、小面；24个味型。'},
    {id:'qian', fam:'J', name:'黔菜', provs:['GZ'], taste:'la', staple:'dao', note:'酸汤鱼、辣子鸡、肠旺面、折耳根、糟辣椒。'},
    {id:'dian', fam:'J', name:'滇菜', provs:['YN'], taste:'la', staple:'dao', note:'过桥米线、汽锅鸡、菌子、鲜花饼、傣味、乳扇。'}
  ]
});
