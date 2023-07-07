#!/usr/local/Cellar/python@3.8/3.8.12_1/bin/python3.8
# -*- coding: utf-8 -*-


import os
import akshare as ak


del os.environ['ALL_PROXY']
# 港股
# ahstocks = ak.stock_zh_ah_name()
# 深证证券交易所股票代码和简称
# ahstocks = ak.stock_info_sz_name_code()
# 上海证券交易所股票代码和简称
ahstocks = ak.stock_info_sh_name_code()
# A 股票
# ahstocks = ak.stock_info_a_code_name()

for stock in ahstocks.values.tolist():
    # 港股,上海,A股票
    sql_str = """INSERT INTO stock (name, code, create_time) VALUES ('{name}', '{code}', UNIX_TIMESTAMP(NOW()) * 1000000);""".format(name=stock[1], code=stock[0])
    # 深圳
    # sql_str = """INSERT INTO stock (name, code, create_time) VALUES ('{name}', '{code}', UNIX_TIMESTAMP(NOW()) * 1000000);""".format(name=stock[2], code=stock[1])
    print(sql_str)
# print(ahstocks)
#
# spot = ak.stock_zh_a_spot_em()
# print(spot)

# daybars = ak.stock_zh_a_daily(symbol="sh603843", start_date="19900101", end_date="20230223", adjust="qfq", )
#
# print('...')

# stock_sh_a_spot_em = ak.stock_sh_a_spot_em()
# stock_sz_a_spot_em = ak.stock_sz_a_spot_em()
# # stock_bj_a_spot_em = ak.stock_bj_a_spot_em()
# H_code_names = ak.stock_hk_spot_em()
#
# # print(H_code_names)
# tencent_bars = ak.stock_hk_hist('00700', period='daily', start_date='19700101', end_date='20230302', adjust='hfq')
# # import pandas as pd
#
# tencent_bars.to_pickle('tencent_day_bars.pkl')
# # print(tencent_bars)
