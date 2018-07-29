#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import json
import traceback

from models import Utils
from models import Database as db
from models.initialize import app, logger


__author__ = 'James Iter'
__date__ = '2018/7/29'
__contact__ = 'james.iter.cn@gmail.com'
__copyright__ = '(c) 2018 by James Iter.'


db.init_conn_redis()


class DataArrangeEngine(object):
    """
    编排规范

    ============== 数据结构 - OHLC Index ===============
    Key@ Z:合约号_周期
    示例@ Z:rb1801_120

    Value@ timestamp OHLCKey
    示例@ 1508204160 H:rb1801_120:20171017:093600

    ================ 数据结构 - OHLC ===================
    Key@ H:合约号_周期:日期:时间
    示例@ H:rb1801_120:20171017:093600

    Value@ {
        'open': open_NO.,
        'high': high_NO.,
        'low': low_NO.,
        'close': close_NO.,
        'last_timestamp': last_timestamp,
        'last_date_time': 'human-readable date time'
    }
    示例@ {
        'open': 3449,
        'high': 3449,
        'low': 3447,
        'close': 3447,
        'last_timestamp': 1508204160,
        'last_date_time': '2017-10-17 09:36:00'
    }
    """

    # rb1801
    contract_code = None

    # 120 (秒)
    granularity = None

    # 3447
    last_price = None

    # 1508204160
    timestamp = None

    @classmethod
    def generate_ohlc_index_key(cls):
        return ':'.join(['Z', cls.contract_code + '_' + cls.granularity])

    @classmethod
    def generate_ohlc_key(cls):

        time_line_timestamp = cls.timestamp + cls.granularity - cls.timestamp % cls.granularity

        # 20171017:093600
        time_line = time.strftime("%Y%m%d:%H%M%S", time.localtime(time_line_timestamp))
        return ':'.join(['H', cls.contract_code + '_' + cls.granularity, time_line])

    @classmethod
    def generate_ohlc_index(cls):
        key = cls.generate_ohlc_index_key()
        score = cls.timestamp
        value = cls.generate_ohlc_key()

        # 可重入，不会产生副作用
        # http://redisdoc.com/sorted_set/zadd.html
        db.r.zadd(key, score, value)

    @classmethod
    def set_ohlc(cls):
        ohlc_key = cls.generate_ohlc_key()
        ohlc = db.r.hgetall(ohlc_key)

        # 2017-10-17 09:36:00
        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cls.timestamp))

        # 如果 ohlc 为空，即空字典 --> {}
        if not ohlc:
            ohlc = {
                'open': cls.last_price,
                'high': cls.last_price,
                'low': cls.last_price,
                'close': cls.last_price,
                'last_timestamp': cls.timestamp,
                'last_date_time': date_time
            }

            db.r.hmset(ohlc_key, ohlc)
            return

        if cls.timestamp <= ohlc['last_timestamp']:
            return

        ohlc['last_timestamp'] = cls.timestamp
        ohlc['last_date_time'] = date_time

        ohlc['close'] = cls.last_price

        if cls.last_price > ohlc['high']:
            ohlc['high'] = cls.last_price

        else:
            ohlc['low'] = cls.last_price

        db.r.hmset(ohlc_key, ohlc)

    @classmethod
    def data_arrange(cls, awp_tick=None):
        """
        数据编排
        :param awp_tick: {
            'granularities': [60, 120, 300, 600, 1800],
            'contract_code': 'rb1801',
            'last_price': 3447,
            'trading_day': '20171017',
            'update_time': '093600'
        }
        :return:
        """

        if not isinstance(awp_tick, dict):
            log = u' '.join([u'数据 --> ', str(awp_tick), u' 需为 json 格式'])
            logger.warning(msg=log)
            return

        if 'granularities' not in awp_tick or not isinstance(awp_tick['granularities'], list):
            log = u'granularities 需为 list 格式'
            logger.warning(msg=log)
            return

        cls.contract_code = awp_tick['contract_code']
        cls.last_price = awp_tick['last_price']
        cls.timestamp = int(time.mktime(time.strptime(
                ' '.join([awp_tick['trading_day'], awp_tick['update_time']]), "%Y%m%d %H%M%S")))

        for granularity in awp_tick['granularities']:
            cls.granularity = granularity
            cls.generate_ohlc_index()
            cls.set_ohlc()

    @classmethod
    def launch(cls):
        while True:
            if Utils.exit_flag:
                msg = 'Thread DataArrangeEngine say bye-bye'
                print msg
                logger.info(msg=msg)

                return

            try:
                awp_tick = db.r.lpop(app.config['data_stream_queue'])

                if awp_tick is None:
                    time.sleep(1)
                    continue

                awp_tick = json.loads(awp_tick)
                cls.data_arrange(awp_tick=awp_tick)

            except AttributeError as e:
                logger.error(traceback.format_exc())
                time.sleep(1)

                if db.r is None:
                    db.init_conn_redis()

            except Exception as e:
                logger.error(traceback.format_exc())
                time.sleep(1)

