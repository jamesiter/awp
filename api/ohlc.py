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

