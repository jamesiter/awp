#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import getopt
import json
import time
import re

from trading_period import TradingPeriod, EXCHANGE_TRADING_PERIOD, FUTURES_TRADING_PERIOD_MAPPING, HOLIDAYS


__author__ = 'James Iter'
__date__ = '2018/4/1'
__contact__ = 'james.iter.cn@gmail.com'
__copyright__ = '(c) 2018 by James Iter.'


def incept_config():
    config = {
        'output_dir': os.getcwd(),
        'granularities': '2,5,10,30,60'
    }

    pattern = re.compile(r'\D*')

    def usage():
        print "Usage:%s [-s] [--data_source]" % sys.argv[0]
        print "-s --data_source, is the path of data file."
        print "-o --output_dir, is the output directory. optional."
        print "-n --name, is the instrument id. optional."
        print "-g --granularities, default are 2,5,10,30,60 minutes, delimiter is a comma. optional."
        print "-b --begin, default is HOLIDAYS first element, format is YYYY-MM-DD. optional."
        print "-e --end, default is today, format is YYYY-MM-DD. optional."

    opts = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hs:o:n:g:b:e:',
                                   ['help', 'data_source=', 'output_dir=', 'name=', 'granularities=', 'begin=', 'end='])
    except getopt.GetoptError as e:
        print str(e)
        usage()
        exit(e.message.__len__())

    for k, v in opts:
        if k in ("-h", "--help"):
            usage()
            exit()

        elif k in ("-s", "--data_source"):
            config['data_source'] = v

        elif k in ("-o", "--output_dir"):
            config['output_dir'] = v

        elif k in ("-n", "--name"):
            config['name'] = v

        elif k in ("-g", "--granularities"):
            config['granularities'] = v

        elif k in ("-b", "--begin"):
            config['begin'] = v

        elif k in ("-e", "--end"):
            config['end'] = v

        else:
            print "unhandled option"

    if 'data_source' not in config:
        print 'Must specify the -s(data_source) arguments.'
        usage()
        exit(1)

    if 'name' not in config:
        config['name'] = os.path.basename(config['data_source']).split('.')[0]

    config['contract_code'] = pattern.match(config['name']).group()

    for granularity in config['granularities'].split(','):

        if not isinstance(config['granularities'], list):
            config['granularities'] = list()

        # 忽略非整数的粒度
        if not granularity.isdigit():
            continue

        else:
            granularity = int(granularity)

        # 粒度小于 2 分钟，或大于 3600 分钟的不予支持
        if 2 > granularity > 3600:
            continue

        config['granularities'].append(granularity)

    if 'begin' not in config:
        config['begin'] = HOLIDAYS[0]

    if 'end' not in config:
        config['end'] = time.strftime('%Y-%m-%d')

    return config


class DateConverter(object):

    def __init__(self):
        self.k_lines = dict()
        # interval: 单位(秒)
        self.interval = 60
        self.last_ts_step = None

    def data_pump(self, depth_market_data=None, save_dir_path=None):
        """
        :param depth_market_data:
        :param save_dir_path: 文件存储目录路径
        :return:
        """
        for key in ['last_price', 'trading_day', 'update_time']:
            if key not in depth_market_data:
                return

        trading_day = depth_market_data['trading_day']
        update_time = depth_market_data['update_time']
        date_time = ' '.join([depth_market_data['trading_day'], depth_market_data['update_time']])
        # ts_step = int(time.mktime(time.strptime(date_time, "%Y%m%d %H:%M:%S"))) / self.interval
        ts_step = int(time.mktime((int(trading_day[:4]), int(trading_day[4:6]), int(trading_day[6:]),
                                   int(update_time[:2]), int(update_time[3:5]), int(update_time[6:]),
                                   0, 0, 0))) / self.interval

        if self.last_ts_step is None:
            self.last_ts_step = ts_step

        if self.last_ts_step != ts_step:
            # 此处可以处理一些边界操作。比如对上一个区间的值做特殊处理等。

            if save_dir_path is not None:
                file_name = self.interval.__str__() + '.json'
                save_path = '/'.join([save_dir_path, file_name])

                if not os.path.isdir(save_dir_path):
                    os.makedirs(save_dir_path, 0755)

                with open(save_path, 'a') as f:
                    f.writelines(json.dumps(self.k_lines, ensure_ascii=False) + '\n')

            self.last_ts_step = ts_step
            self.k_lines = dict()

        last_price = depth_market_data['last_price']

        if 'open' not in self.k_lines:
            self.k_lines = {
                'open': last_price,
                'high': last_price,
                'low': last_price,
                'close': last_price,
                'date_time': date_time
            }

        self.k_lines['close'] = last_price

        if last_price > self.k_lines['high']:
            self.k_lines['high'] = last_price

        elif last_price < self.k_lines['low']:
            self.k_lines['low'] = last_price

        else:
            pass


def trading_time_filter(date_time=None, contract_code=None, exchange_trading_period_by_ts=None):
    ts = int(time.mktime(time.strptime(date_time, "%Y-%m-%d %H:%M:%S")))
    contract_trading_period_ts = list()

    for trading_period in FUTURES_TRADING_PERIOD_MAPPING[contract_code]:
        contract_trading_period_ts.extend(
            exchange_trading_period_by_ts[trading_period.exchange_code][trading_period.period])

    for trading_period_ts in contract_trading_period_ts:
        if trading_period_ts[0] <= ts <= trading_period_ts[1]:
            return True

    return False


def run():
    config = incept_config()
    workdays = TradingPeriod.get_workdays(begin=config['begin'], end=config['end'])
    workdays_exchange_trading_period_by_ts = \
        TradingPeriod.get_workdays_exchange_trading_period(
            _workdays=workdays, exchange_trading_period=EXCHANGE_TRADING_PERIOD)

    date_converters = list()

    for granularity in config['granularities']:
        date_converter = DateConverter()
        date_converter.interval = 60 * granularity
        date_converters.append(date_converter)

    with open(config['data_source']) as f:
        for i, line in enumerate(f):

            # 忽略 csv 头
            if i == 0:
                continue

            depth_market_data = dict()
            row = line.split(',')
            date_time = row[0].split(' ')

            str_date = '-'.join(date_time[0].split('/'))

            if str_date not in workdays_exchange_trading_period_by_ts:
                continue

            if not trading_time_filter(date_time=' '.join([str_date, date_time[1]]),
                                       contract_code=config['contract_code'],
                                       exchange_trading_period_by_ts=workdays_exchange_trading_period_by_ts[str_date]):
                continue

            depth_market_data['trading_day'] = ''.join(date_time[0].split('/'))
            depth_market_data['update_time'] = date_time[1]

            if row[4].isdigit():
                depth_market_data['last_price'] = int(row[4])
            else:
                try:
                    depth_market_data['last_price'] = float(row[4])
                except ValueError:
                    continue

            for date_converter in date_converters:
                date_converter.data_pump(depth_market_data=depth_market_data, save_dir_path=config['output_dir'])


if __name__ == '__main__':
    run()

