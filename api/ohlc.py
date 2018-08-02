#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Blueprint
import jimit as ji

from models import Utils
from models import OHLCIndex
from models import OHLC


__author__ = 'James Iter'
__date__ = '2018/8/1'
__contact__ = 'james.iter.cn@gmail.com'
__copyright__ = '(c) 2018 by James Iter.'


blueprint = Blueprint(
    'api_ohlc',
    __name__,
    url_prefix='/api/ohlc'
)

blueprints = Blueprint(
    'api_ohlcs',
    __name__,
    url_prefix='/api/ohlcs'
)


@Utils.dumps2response
def r_get(contract_code, granularity):
    ret = dict()
    ret['state'] = ji.Common.exchange_state(20000)

    ohlc_index = OHLCIndex()
    ohlc_index.contract_code = contract_code
    ohlc_index.granularity = granularity
    ohlc_index.get_ohlc_index_key()

    ohlc_keys = ohlc_index.get_by_range(start=0, end=-1)

    ret['data'] = OHLC.get_by_ohlc_keys(ohlc_keys=ohlc_keys)

    return ret


@Utils.dumps2response
def r_get_by_range(contract_code, granularity, start, end):
    ret = dict()
    ret['state'] = ji.Common.exchange_state(20000)

    ohlc_index = OHLCIndex()
    ohlc_index.contract_code = contract_code
    ohlc_index.granularity = granularity
    ohlc_index.get_ohlc_index_key()

    if not ohlc_index.exist():
        ret['state'] = ji.Common.exchange_state(40401)
        return ret

    if not ohlc_index.z_type():
        ret['state'] = ji.Common.exchange_state(41202)
        return ret

    ohlc_keys = ohlc_index.get_by_range(start=start, end=end)

    ret['data'] = OHLC.get_by_ohlc_keys(ohlc_keys=ohlc_keys)

    return ret


@Utils.dumps2response
def r_get_by_score(contract_code, granularity, _min, _max):
    ret = dict()
    ret['state'] = ji.Common.exchange_state(20000)

    ohlc_index = OHLCIndex()
    ohlc_index.contract_code = contract_code
    ohlc_index.granularity = granularity
    ohlc_index.get_ohlc_index_key()

    if not ohlc_index.exist():
        ret['state'] = ji.Common.exchange_state(40401)
        return ret

    if not ohlc_index.z_type():
        ret['state'] = ji.Common.exchange_state(41202)
        return ret

    ohlc_keys = ohlc_index.get_by_score(_min=_min, _max=_max)

    ret['data'] = OHLC.get_by_ohlc_keys(ohlc_keys=ohlc_keys)

    return ret


@Utils.dumps2response
def r_hhv_by_range(contract_code, granularity, start, end, step):
    ret = dict()
    ret['state'] = ji.Common.exchange_state(20000)

    ohlc_index = OHLCIndex()
    ohlc_index.contract_code = contract_code
    ohlc_index.granularity = granularity
    ohlc_index.get_ohlc_index_key()

    if not ohlc_index.exist():
        ret['state'] = ji.Common.exchange_state(40401)
        return ret

    if not ohlc_index.z_type():
        ret['state'] = ji.Common.exchange_state(41202)
        return ret

    ohlc_keys = ohlc_index.get_by_range(start=start, end=end)

    c = list()
    for ohlc in OHLC.get_by_ohlc_keys(ohlc_keys=ohlc_keys):
        c.append(ohlc['high'])

    ret['data'] = OHLC.hhv(series=c, step=int(step))

    return ret


@Utils.dumps2response
def r_llv_by_range(contract_code, granularity, start, end, step):
    ret = dict()
    ret['state'] = ji.Common.exchange_state(20000)

    ohlc_index = OHLCIndex()
    ohlc_index.contract_code = contract_code
    ohlc_index.granularity = granularity
    ohlc_index.get_ohlc_index_key()

    if not ohlc_index.exist():
        ret['state'] = ji.Common.exchange_state(40401)
        return ret

    if not ohlc_index.z_type():
        ret['state'] = ji.Common.exchange_state(41202)
        return ret

    ohlc_keys = ohlc_index.get_by_range(start=start, end=end)

    c = list()
    for ohlc in OHLC.get_by_ohlc_keys(ohlc_keys=ohlc_keys):
        c.append(ohlc['high'])

    ret['data'] = OHLC.llv(series=c, step=int(step))

    return ret


@Utils.dumps2response
def r_hhv_llv_cross_up_by_range(contract_code, granularity, start, end, steps):
    ret = dict()
    ret['state'] = ji.Common.exchange_state(20000)

    ohlc_index = OHLCIndex()
    ohlc_index.contract_code = contract_code
    ohlc_index.granularity = granularity
    ohlc_index.get_ohlc_index_key()

    if not ohlc_index.exist():
        ret['state'] = ji.Common.exchange_state(40401)
        return ret

    if not ohlc_index.z_type():
        ret['state'] = ji.Common.exchange_state(41202)
        return ret

    ohlc_keys = ohlc_index.get_by_range(start=start, end=end)

    c = list()
    for ohlc in OHLC.get_by_ohlc_keys(ohlc_keys=ohlc_keys):
        c.append(ohlc['high'])

    steps = steps.split(',')

    if steps.__len__() < 2:
        steps.append(steps[0])

    _h = OHLC.llv(series=c, step=int(steps[0]))
    _l = OHLC.llv(series=c, step=int(steps[1]))

    ret['data'] = OHLC.cross_up(series_a=_h, series_b=_l)

    return ret


@Utils.dumps2response
def r_hhv_llv_cross_down_by_range(contract_code, granularity, start, end, steps):
    ret = dict()
    ret['state'] = ji.Common.exchange_state(20000)

    ohlc_index = OHLCIndex()
    ohlc_index.contract_code = contract_code
    ohlc_index.granularity = granularity
    ohlc_index.get_ohlc_index_key()

    if not ohlc_index.exist():
        ret['state'] = ji.Common.exchange_state(40401)
        return ret

    if not ohlc_index.z_type():
        ret['state'] = ji.Common.exchange_state(41202)
        return ret

    ohlc_keys = ohlc_index.get_by_range(start=start, end=end)

    c = list()
    for ohlc in OHLC.get_by_ohlc_keys(ohlc_keys=ohlc_keys):
        c.append(ohlc['high'])

    steps = steps.split(',')

    if steps.__len__() < 2:
        steps.append(steps[0])

    _h = OHLC.llv(series=c, step=int(steps[0]))
    _l = OHLC.llv(series=c, step=int(steps[1]))

    ret['data'] = OHLC.cross_down(series_a=_h, series_b=_l)

    return ret
