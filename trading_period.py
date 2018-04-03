#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 交易时段


from itertools import chain


__author__ = 'James Iter'
__date__ = '2018/4/3'
__contact__ = 'james.iter.cn@gmail.com'
__copyright__ = '(c) 2018 by James Iter.'


# 周末补班
MAKE_UP_DAYS = [
    "2017-01-22",
    "2017-02-04",
    "2017-04-01",
    "2017-05-27",
    "2017-09-30",

    "2018-02-11",
    "2018-02-24",
    "2018-04-08",
    "2018-04-28",
    "2018-09-29",
    "2018-09-30"
]

# 公共假日
HOLIDAYS = [
    "2016-12-31",
    "2017-01-01",
    "2017-01-02",

    "2017-01-27",
    "2017-01-28",
    "2017-01-29",
    "2017-01-30",
    "2017-01-31",
    "2017-02-01",
    "2017-02-02",

    "2017-04-01",
    "2017-04-02",
    "2017-04-03",
    "2017-04-04",
    
    "2017-04-29",
    "2017-04-30",
    "2017-05-01",
    
    "2017-05-27",
    "2017-05-28",
    "2017-05-29",
    "2017-05-30",
    
    "2017-09-30",
    "2017-10-01",
    "2017-10-02",
    "2017-10-03",
    "2017-10-04",
    "2017-10-05",
    "2017-10-06",
    "2017-10-07",
    "2017-10-08",
    
    "2017-12-30",
    "2017-12-31",
    "2018-01-01",
    
    "2018-02-15",
    "2018-02-16",
    "2018-02-17",
    "2018-02-18",
    "2018-02-19",
    "2018-02-20",
    "2018-02-21",
    
    "2018-04-05",
    "2018-04-06",
    "2018-04-07",
    "2018-04-08",
    
    "2018-04-28",
    "2018-04-29",
    "2018-04-30",
    "2018-05-01",
    
    "2018-06-16",
    "2018-06-17",
    "2018-06-18",
    
    "2018-09-22",
    "2018-09-23",
    "2018-09-24",
    
    "2018-09-29",
    "2018-09-30",
    "2018-10-01",
    "2018-10-02",
    "2018-10-03",
    "2018-10-04",
    "2018-10-05",
    "2018-10-06",
    "2018-10-07"
]

# 中国金融期货交易所 股指期货交易时间
# http://www.cffex.com.cn
CFFEX_STOCK_INDEX = {
    'daytime': [('09:25:00', '11:30:00'), ('13:00:00', '15:00:00')]
}

# 中国金融期货交易所 国债期货交易时间
# http://www.cffex.com.cn
CFFEX_NATIONAL_DEBT = {
    'daytime': [('09:10:00', '11:30:00'), ('13:00:00', '15:15:00')]
}

# 郑州商品交易所交易时间
# http://www.czce.com.cn
CZCE = {
    'daytime': [('08:55:00', '10:15:01'), ('10:30:00', '11:30:00'), ('13:30:00', '15:00:00')],
    'night': [('20:55:00', '23:30:00')]
}

# 上海期货交易所交易时间
# http://www.shfe.com.cn
SHFE = {
    'daytime': CZCE['daytime'],
    'night_group_01': [('20:55:00', '02:30:00')],
    'night_group_02': [('20:55:00', '01:00:00')],
    'night_group_03': [('20:55:00', '23:00:00')]
}

# 大连商品交易所交易时间
# http://www.dce.com.cn
DCE = CZCE

# 上海国际能源交易所交易时间
# http://www.ine.cn
INE = {
    'daytime': CZCE['daytime'],
    'night': SHFE['night_group_01']
}

futures_trading_period_mapping = {
    # 中金所
    "IC": CFFEX_STOCK_INDEX['daytime'],     # 中证500股指
    "IF": CFFEX_STOCK_INDEX['daytime'],     # 沪深300股指
    "IH": CFFEX_STOCK_INDEX['daytime'],     # 上证50股指
    "TF": CFFEX_NATIONAL_DEBT['daytime'],   # 5年国债
    "T": CFFEX_NATIONAL_DEBT['daytime'],    # 10年国债

    # 郑商所
    "CF": list(chain(CZCE['daytime'], CZCE['night'])),      # 棉花
    "ZC": list(chain(CZCE['daytime'], CZCE['night'])),      # 动力煤
    "SR": list(chain(CZCE['daytime'], CZCE['night'])),      # 白砂糖
    "RM": list(chain(CZCE['daytime'], CZCE['night'])),      # 菜籽粕
    "MA": list(chain(CZCE['daytime'], CZCE['night'])),      # 甲醇
    "TA": list(chain(CZCE['daytime'], CZCE['night'])),      # PTA化纤
    "FG": list(chain(CZCE['daytime'], CZCE['night'])),      # 玻璃
    "OI": list(chain(CZCE['daytime'], CZCE['night'])),      # 菜籽油
    "CY": list(chain(CZCE['daytime'], CZCE['night'])),      # 棉纱
    "WH": CZCE['daytime'],                                  # 强筋麦709
    "SM": CZCE['daytime'],                                  # 锰硅709
    "SF": CZCE['daytime'],                                  # 硅铁709
    "RS": CZCE['daytime'],                                  # 油菜籽709
    "RI": CZCE['daytime'],                                  # 早籼稻709
    "PM": CZCE['daytime'],                                  # 普通小麦709
    "LR": CZCE['daytime'],                                  # 晚籼稻709
    "JR": CZCE['daytime'],                                  # 粳稻709
    "AP": CZCE['daytime'],                                  # 苹果

    # 大商所
    "j": list(chain(DCE['daytime'], DCE['night'])),         # 焦炭
    "i": list(chain(DCE['daytime'], DCE['night'])),         # 铁矿石
    "jm": list(chain(DCE['daytime'], DCE['night'])),        # 焦煤
    "a": list(chain(DCE['daytime'], DCE['night'])),         # 黄大豆1号
    "y": list(chain(DCE['daytime'], DCE['night'])),         # 豆油
    "m": list(chain(DCE['daytime'], DCE['night'])),         # 豆粕
    "b": list(chain(DCE['daytime'], DCE['night'])),         # 黄大豆2号
    "p": list(chain(DCE['daytime'], DCE['night'])),         # 棕榈油

    "jd": DCE['daytime'],                                   # 鲜鸡蛋1709
    "l": DCE['daytime'],                                    # 聚乙烯1709
    "v": DCE['daytime'],                                    # 聚氯乙烯1709
    "pp": DCE['daytime'],                                   # 聚丙烯1709
    "fb": DCE['daytime'],                                   # 纤维板1709
    "cs": DCE['daytime'],                                   # 玉米淀粉1709
    "c": DCE['daytime'],                                    # 黄玉米1709
    "bb": DCE['daytime'],                                   # 胶合板1709

    # 上期所
    "ag": list(chain(SHFE['daytime'], SHFE['night_group_01'])),  # 白银1709
    "au": list(chain(SHFE['daytime'], SHFE['night_group_01'])),  # 黄金1710

    "pb": list(chain(SHFE['daytime'], SHFE['night_group_02'])),  # 铅1709
    "ni": list(chain(SHFE['daytime'], SHFE['night_group_02'])),  # 镍1709
    "zn": list(chain(SHFE['daytime'], SHFE['night_group_02'])),  # 锌1709
    "al": list(chain(SHFE['daytime'], SHFE['night_group_02'])),  # 铝1709
    "sn": list(chain(SHFE['daytime'], SHFE['night_group_02'])),  # 锡1709
    "cu": list(chain(SHFE['daytime'], SHFE['night_group_02'])),  # 铜1709

    "ru": list(chain(SHFE['daytime'], SHFE['night_group_03'])),  # 天然橡胶1709
    "rb": list(chain(SHFE['daytime'], SHFE['night_group_03'])),  # 螺纹钢1709
    "hc": list(chain(SHFE['daytime'], SHFE['night_group_03'])),  # 热轧板1709
    "bu": list(chain(SHFE['daytime'], SHFE['night_group_03'])),  # 沥青1809

    "wr": SHFE['daytime'],                                       # 线材1709
    "fu": SHFE['daytime'],                                       # 燃料油1709

    # 能源所
    "sc": list(chain(INE['daytime'], INE['night'])),            # 螺纹钢1709
}

