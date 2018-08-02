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

    @staticmethod
    def hhv(series=None, step=None):

        assert isinstance(series, list)
        assert 0 < step <= series.__len__()

        numbers = list()
        stack = list()

        for number in series:
            stack.append(number)

            if stack.__len__() > step:
                stack = stack[0 - step:]

            numbers.append(max(stack))

        return numbers

    @staticmethod
    def llv(series=None, step=None):

        assert isinstance(series, list)
        assert 0 < step <= series.__len__()

        numbers = list()
        stack = list()

        for number in series:
            stack.append(number)

            if stack.__len__() > step:
                stack = stack[0 - step:]

            numbers.append(min(stack))

        return numbers

    @staticmethod
    def cross_up(series_a=None, series_b=None):

        assert isinstance(series_a, list)
        assert isinstance(series_b, list)
        assert series_a.__len__() == series_b.__len__()

        cross_series = list()

        for i, v in enumerate(series_a):
            if i > 0:
                if series_a[i] > series_b[i] and series_a[i - 1] <= series_b[i - 1]:
                    cross_series.append(True)
                    continue

            cross_series.append(None)

        return cross_series

    @staticmethod
    def cross_down(series_a=None, series_b=None):

        assert isinstance(series_a, list)
        assert isinstance(series_b, list)
        assert series_a.__len__() == series_b.__len__()

        cross_series = list()

        for i, v in enumerate(series_a):
            if i > 0:
                if series_a[i] < series_b[i] and series_a[i - 1] >= series_b[i - 1]:
                    cross_series.append(True)
                    continue

            cross_series.append(None)

        return cross_series

