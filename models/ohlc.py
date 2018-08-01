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


class OHLC(object):

    def __init__(self):
        pass

    @staticmethod
    def get_by_ohlc_keys(ohlc_keys=None):

        with db.r.pipeline() as pipe:
            for ohlc_key in ohlc_keys:
                pipe.hgetall(ohlc_key)

            return pipe.execute()

