#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import getopt
import json
import time
import re

from k_line_pump import KLinePump
from data_converter import trading_time_filter
from trading_period import TradingPeriod, EXCHANGE_TRADING_PERIOD, HOLIDAYS


__author__ = 'James Iter'
__date__ = '2018/4/6'
__contact__ = 'james.iter.cn@gmail.com'
__copyright__ = '(c) 2018 by James Iter.'


DEPOSITARY_OF_KLINE = dict()
instrument_id_interval_pattern = re.compile(r'(\D*\d+)_(\d+)\.json')
contract_code_pattern = re.compile(r'\D*')


def incept_config():
    _config = {
        'granularities': '2,5,10,30,60',
        'config_file': './data_sewing_machine.config'
    }

    def usage():
        print "Usage:%s [-s] [--data_source_dir]" % sys.argv[0]
        print "-s --data_source_dir, is the path of data file directory."
        print "-g --granularities, default are 2,5,10,30,60 minutes, delimiter is a comma. optional."
        print "-c --config. optional."

    opts = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hs:b:e:g:c:',
                                   ['help', 'data_source_dir=', 'begin=', 'end=', 'granularities=', 'config='])
    except getopt.GetoptError as e:
        print str(e)
        usage()
        exit(e.message.__len__())

    for k, v in opts:
        if k in ("-h", "--help"):
            usage()
            exit()

        elif k in ("-s", "--data_source_dir"):
            _config['data_source_dir'] = v

        elif k in ("-b", "--begin"):
            _config['begin'] = v

        elif k in ("-e", "--end"):
            _config['end'] = v

        elif k in ("-g", "--granularities"):
            _config['granularities'] = v

        elif k in ("-c", "--config"):
            _config['config_file'] = v

        else:
            print "unhandled option"

    if 'config_file' in _config:
        with open(_config['config_file'], 'r') as f:
            _config.update(json.load(f))

    if 'data_source_dir' not in _config:
        print 'Must specify the -s(data_source_dir) arguments.'
        usage()
        exit(1)

    if 'begin' not in _config:
        _config['begin'] = HOLIDAYS[0]

    if 'end' not in _config:
        _config['end'] = time.strftime('%Y-%m-%d')

    for granularity in _config['granularities'].split(','):

        if not isinstance(_config['granularities'], list):
            _config['granularities'] = list()

        # 忽略非整数的粒度
        if not granularity.isdigit():
            continue

        else:
            granularity = int(granularity)

        # 粒度小于 2 分钟，或大于 3600 分钟的不予支持
        if 2 > granularity > 3600:
            continue

        _config['granularities'].append(granularity)

    return _config


def load_data_from_file():

    for file_name in os.listdir(config['data_source_dir']):
        p = instrument_id_interval_pattern.match(file_name)

        if p is not None:
            fields = p.groups()

            if fields[0] not in DEPOSITARY_OF_KLINE:
                DEPOSITARY_OF_KLINE[fields[0]] = dict()

            if fields[1] not in DEPOSITARY_OF_KLINE[fields[0]]:
                DEPOSITARY_OF_KLINE[fields[0]][fields[1]] = {
                    'path': os.path.join(config['data_source_dir'], file_name),
                    'data': list()
                }

    for k, v in DEPOSITARY_OF_KLINE.items():

        for _k, _v in v.items():
            with open(_v['path'], 'r') as f:
                for line in f:
                    DEPOSITARY_OF_KLINE[k][_k]['data'].append(json.loads(line.strip()))


def init_k_line_pump():

    for k, v in DEPOSITARY_OF_KLINE.items():
        for _k, _v in v.items():
            DEPOSITARY_OF_KLINE[k][_k]['k_line_pump'] = KLinePump()
            DEPOSITARY_OF_KLINE[k][_k]['k_line_pump'].interval = int(_k)


config = incept_config()
load_data_from_file()
init_k_line_pump()

workdays = TradingPeriod.get_workdays(begin=config['begin'], end=config['end'])
workdays_exchange_trading_period_by_ts = \
    TradingPeriod.get_workdays_exchange_trading_period(
        _workdays=workdays, exchange_trading_period=EXCHANGE_TRADING_PERIOD)


def sewing_data_to_file_and_depositary(depth_market_data=None):

    for key in ['InstrumentID', 'LastPrice', 'TradingDay', 'UpdateTime']:
        if not hasattr(depth_market_data, key):
            return

    instrument_id = depth_market_data.InstrumentID
    contract_code = contract_code_pattern.match(instrument_id).group()
    date = '-'.join([depth_market_data.TradingDay[:4], depth_market_data.TradingDay[4:6],
                     depth_market_data.TradingDay[6:]])

    date_time = ' '.join([date, depth_market_data.UpdateTime])

    if not trading_time_filter(
            date_time=date_time, contract_code=contract_code,
            exchange_trading_period_by_ts=workdays_exchange_trading_period_by_ts[date]):
        return

    formatted_depth_market_data = dict()
    formatted_depth_market_data['trading_day'] = date.replace('-', '')
    formatted_depth_market_data['update_time'] = depth_market_data.UpdateTime
    formatted_depth_market_data['instrument_id'] = instrument_id

    if isinstance(depth_market_data.LastPrice, basestring):
        if depth_market_data.LastPrice.isdigit():
            formatted_depth_market_data['last_price'] = int(depth_market_data.LastPrice)
        else:
            try:
                formatted_depth_market_data['last_price'] = float(depth_market_data.LastPrice)
            except ValueError:
                return

    else:
        formatted_depth_market_data['last_price'] = depth_market_data.LastPrice

    if instrument_id not in DEPOSITARY_OF_KLINE:
        DEPOSITARY_OF_KLINE[instrument_id] = dict()

    for granularity in config['granularities']:
        interval = 60 * granularity
        str_interval = str(interval)

        if str_interval not in DEPOSITARY_OF_KLINE[instrument_id]:
            file_name = '_'.join([instrument_id, str_interval]) + '.json'
            DEPOSITARY_OF_KLINE[instrument_id][str_interval] = {
                'path': os.path.join(config['data_source_dir'], file_name),
                'data': list()
            }
            DEPOSITARY_OF_KLINE[instrument_id][str_interval]['k_line_pump'] = KLinePump()
            DEPOSITARY_OF_KLINE[instrument_id][str_interval]['k_line_pump'].interval = interval

    for k, v in DEPOSITARY_OF_KLINE[instrument_id].items():
        DEPOSITARY_OF_KLINE[instrument_id][k]['k_line_pump'].process_data(
            depth_market_data=formatted_depth_market_data, save_path=DEPOSITARY_OF_KLINE[instrument_id][k]['path'])

        if DEPOSITARY_OF_KLINE[instrument_id][k]['k_line_pump'].str_k_line is not None:
            DEPOSITARY_OF_KLINE[instrument_id][k]['data'].append(
                json.loads(DEPOSITARY_OF_KLINE[instrument_id][k]['k_line_pump'].str_k_line))

            DEPOSITARY_OF_KLINE[instrument_id][k]['k_line_pump'].str_k_line = None


def get_k_line_column(instrument_id=None, interval=None, ohlc='high', depth=0):
    """
    :param instrument_id: 合约名称。
    :param interval: 取样间隔。
    :param ohlc: [Open|High|Low|Close]。
    :param depth: 深度。默认 0 将获取所有。
    :return: list。
    """

    ohlc = ohlc.lower()

    assert ohlc in ['open', 'high', 'low', 'close']

    k_line_column = list()
    str_interval = str(interval)
    max_depth = DEPOSITARY_OF_KLINE[instrument_id][str_interval]['data'].__len__()
    if depth == 0 or depth >= max_depth:
        depth = max_depth

    depth = 0 - depth

    for i in range(depth, 0):
        k_line_column.append(DEPOSITARY_OF_KLINE[instrument_id][str_interval]['data'][i][ohlc])

    return k_line_column


def test():
    from collections import namedtuple

    DepthMarketData = namedtuple('DepthMarketData', 'TradingDay InstrumentID LastPrice UpdateTime')

    data_s = list()
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3445, UpdateTime='11:17:34'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3447, UpdateTime='11:17:34'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3443, UpdateTime='11:17:35'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3440, UpdateTime='11:17:36'))

    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3345, UpdateTime='11:18:34'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3347, UpdateTime='11:18:34'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3243, UpdateTime='11:18:35'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3450, UpdateTime='11:18:36'))

    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3245, UpdateTime='11:19:34'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3247, UpdateTime='11:19:34'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3243, UpdateTime='11:19:35'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3250, UpdateTime='11:19:36'))

    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3545, UpdateTime='11:20:34'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3347, UpdateTime='11:20:34'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3243, UpdateTime='11:20:35'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3400, UpdateTime='11:20:36'))

    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3145, UpdateTime='11:21:34'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3047, UpdateTime='11:21:34'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3643, UpdateTime='11:21:35'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3200, UpdateTime='11:21:36'))

    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3545, UpdateTime='11:22:34'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3047, UpdateTime='11:22:34'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3443, UpdateTime='11:22:35'))
    data_s.append(DepthMarketData(TradingDay='20180327', InstrumentID='rb1805', LastPrice=3500, UpdateTime='11:22:36'))

    for data in data_s:
        sewing_data_to_file_and_depositary(depth_market_data=data)

    new_k_line_col = get_k_line_column(instrument_id='rb1805', interval=120, ohlc='high', depth=10)

    pass


test()
