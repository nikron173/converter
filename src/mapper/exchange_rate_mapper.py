import json
from decimal import Decimal
from typing import Dict

from src.entity.exchange_rate import ExchangeRate
from src.mapper.currency_mapper import object_to_currency
from src.mapper.currency_mapper import get_currency_from_dict


def object_to_exchange_rate(**kwargs) -> ExchangeRate:
    base_currency = object_to_currency(
        id=kwargs.get('b_id'),
        code=kwargs.get('b_code'),
        full_name=kwargs.get('b_full_name'),
        sign=kwargs.get('b_sign')
    )
    target_currency = object_to_currency(
        id=kwargs.get('t_id'),
        code=kwargs.get('t_code'),
        full_name=kwargs.get('t_full_name'),
        sign=kwargs.get('t_sign')
    )
    exchange_rate = ExchangeRate(kwargs.get('e_id'), base_currency, target_currency, Decimal(kwargs.get('e_rate')))
    return exchange_rate


# def form_to_exchange_rate(data: str) -> ExchangeRate:
#     exchange_rate_data = {}
#     for parameter in data.split('&'):
#         key, value = parameter.split('=')
#         exchange_rate_data[key] = unquote(value)
#     return get_data_dict(exchange_rate_data)


def json_to_exchange_rate(data: str) -> ExchangeRate:
    dict_data = json.loads(data)
    return get_data_dict(dict_data)


def get_data_dict(data: Dict) -> ExchangeRate:
    exchange_rate = ExchangeRate()
    exchange_rate.base = get_currency_from_dict(data.get('baseCurrency'))
    exchange_rate.target = get_currency_from_dict(data.get('targetCurrency'))
    exchange_rate.rate = Decimal(data.get('rate'))
    if exchange_rate.rate:
        return exchange_rate
    raise Exception(f'Заданы не все параметры обменника')
