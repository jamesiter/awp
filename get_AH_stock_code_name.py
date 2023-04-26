import akshare as ak

ahstocks = ak.stock_zh_ah_name()

print(len(ahstocks))
#
# spot = ak.stock_zh_a_spot_em()
# print(spot)

# daybars = ak.stock_zh_a_daily(symbol="sh603843", start_date="19900101", end_date="20230223", adjust="qfq", )
#
# print('...')

stock_sh_a_spot_em = ak.stock_sh_a_spot_em()
stock_sz_a_spot_em = ak.stock_sz_a_spot_em()
# stock_bj_a_spot_em = ak.stock_bj_a_spot_em()
H_code_names=ak.stock_hk_spot_em()

print('...', len(H_code_names))
tencent_bars=ak.stock_hk_hist('00700', period='daily', start_date='19700101', end_date='20230302', adjust='hfq')
# import pandas as pd

tencent_bars.to_pickle('tencent_day_bars.pkl')
print(len(tencent_bars))
