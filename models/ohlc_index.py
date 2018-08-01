#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
from flask import g

from initialize import app
from models import Database as db


__author__ = 'James Iter'
__date__ = '2018/8/1'
__contact__ = 'james.iter.cn@gmail.com'
__copyright__ = '(c) 2018 by James Iter.'


class OHLCIndex(object):

    def __init__(self):
        self.contract_code = None
        self.granularity = None
        self.ohlc_index_key = None

    def get_ohlc_index_key(self):
        self.ohlc_index_key = ':'.join(['Z', self.contract_code + '_' + self.granularity.__str__()])
        return self.ohlc_index_key

    def exist(self):
        return db.r.exists(self.ohlc_index_key)

    def z_type(self):
        return db.r.type(self.ohlc_index_key) == 'zset'

    def get_border(self):

        ret = db.r.zrange(self.ohlc_index_key, 0, 0, withscores=True)[0][1]

        _min = _max = 0

        if ret:
            _min = ret[0][1]

        else:
            return _min, _max

        ret = db.r.zrange(self.ohlc_index_key, -1, -1, withscores=True)[0][1]

        if ret:
            _max = ret[0][1]

        return _min, _max

    def get_by_range(self, start=0, end=-1):
        return db.r.zrange(self.ohlc_index_key, start, end)

    def get_by_score(self, _min=0, _max=-1):
        return db.r.zrangebyscore(self.ohlc_index_key, min=_min, max=_max)

