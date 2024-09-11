import http.client

from src.repository.currency_repository import CurrencyRepository
from src.handler import MainHandler
from src.mapper.currency_mapper import *
from src.util.parse_query import get_length_and_content_type
from src.error.application_error import ApplicationError


class CurrencyService:
    def __init__(self, currency_repository: CurrencyRepository):
        self._currency_repository = currency_repository

    def get_currency(self, request: MainHandler):
        code = request.path.split('/')[-1].upper()
        currency = self._currency_repository.find_by_code(code)
        if currency is None:
            raise ApplicationError(f'Валюта \'{code}\' не найдена', http.client.NOT_FOUND)
        return json.dumps(currency.to_dict()).encode('utf-8')

    def get_currencies(self, request=None):
        currencies = self._currency_repository.find_all()
        return json.dumps([currency.to_dict() for currency in currencies]).encode('utf-8')

    def save_currency(self, request: MainHandler):
        length, content_types = get_length_and_content_type(request.headers)

        data = request.rfile.read(length).decode('utf-8')
        match content_types:
            case _ if 'application/x-www-form-urlencoded' in content_types:
                currency = form_to_currency(data)
            case _ if 'application/json' in content_types:
                currency = json_to_currency(data)
            case _:
                raise ApplicationError(f'Не известный Content-Type - {content_types}',
                                       http.client.BAD_REQUEST)

        check_currency = self._currency_repository.find_by_code(currency.code)
        if check_currency is not None:
            raise ApplicationError(f'Валюта \'{currency.code}\' уже существует',
                                   http.client.BAD_REQUEST)

        return json.dumps(self._currency_repository.save(currency).to_dict()).encode('utf-8')
