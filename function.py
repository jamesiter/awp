#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import re
import json


__author__ = 'James Iter'
__date__ = '2018/5/13'
__contact__ = 'james.iter.cn@gmail.com'
__copyright__ = '(c) 2018 by James Iter.'


def load_data_from_file(instruments_id=None, granularities=None, data_source_dir='./'):

    ret = dict()
    files_name = list()
    instrument_id_interval_pattern = re.compile(r'(\D*\d+)_(\d+)\.json')

    if instruments_id is not None and granularities is not None:
        for instrument_id in instruments_id.split(','):
            for granularity in granularities.replace(' ', '').split(','):

                file_name = '_'.join([instrument_id, granularity]) + '.json'

                files_name.append(file_name)

    else:
        for file_name in os.listdir(data_source_dir):
            files_name.append(file_name)

    for file_name in files_name:
        p = instrument_id_interval_pattern.match(file_name)

        if p is not None:
            fields = p.groups()
            key = '_'.join([fields[0], fields[1]])

            if key not in ret:
                ret[key] = list()

    for k, v in ret.items():
        file_path = os.path.join(data_source_dir, k + '.json')

        if not os.path.isfile(file_path):
            continue

        with open(file_path, 'r') as f:
            for line in f:
                json_k_line = json.loads(line.strip())
                ret[k].append(json_k_line)

    return ret


def get_k_line_column(data=None, instrument_id=None, interval=None, ohlc='high', depth=0):
    """
    :param data: 数据源
    :param instrument_id: 合约名称。
    :param interval: 取样间隔。
    :param ohlc: [Open|High|Low|Close]。
    :param depth: 深度。默认 0 将获取所有。
    :return: list。
    """

    ohlc = ohlc.lower()

    assert ohlc in ['open', 'high', 'low', 'close']

    ret = list()
    str_interval = str(interval)
    key = '_'.join([instrument_id, str_interval])
    max_depth = data[key].__len__()
    if depth == 0 or depth >= max_depth:
        depth = max_depth

    depth = 0 - depth

    for i in range(depth, 0):
        ret.append((data[key][i][ohlc], data[key][i]['date_time']))

    return ret


def get_last_k_line(data=None, instrument_id=None, interval=None):
    """
    :param data: 数据源
    :param instrument_id: 合约名称。
    :param interval: 取样间隔。
    :return: dict。
    """

    str_interval = str(interval)
    key = '_'.join([instrument_id, str_interval])

    if 1 > data[key].__len__():
        return None

    return data[key][-1]


