import json
import urllib.parse
from typing import Dict
from http.client import BAD_REQUEST

from src.entity.currency import Currency
from src.error.application_error import ApplicationError


def object_to_currency(**kwargs) -> Currency:
    return Currency(kwargs.get('id'), kwargs.get('code'), kwargs.get('full_name'), kwargs.get('sign'))


def form_to_currency(data: str) -> Currency:
    currency_data = {}
    for parameter in data.split('&'):
        key, value = parameter.split('=')
        currency_data[key] = urllib.parse.unquote(value)
    return get_currency_from_dict(currency_data)


def json_to_currency(data: str) -> Currency:
    dict_data = json.loads(data)
    print(dict_data)
    return get_currency_from_dict(dict_data)


def get_currency_from_dict(data: Dict) -> Currency:
    currency = Currency()
    currency.code = data.get('code')
    currency.full_name = data.get('name')
    currency.sign = data.get('sign')
    if currency.code and currency.full_name and currency.sign:
        return currency
    raise ApplicationError(f'Заданы не все параметры валюты', BAD_REQUEST)
