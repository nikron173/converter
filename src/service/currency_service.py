from src.repository.currency_repository import CurrencyRepository
from src.handler import MainHandler
from src.mapper.currency_mapper import *


class CurrencyService:
    def __init__(self, currency_repository: CurrencyRepository):
        self._currency_repository = currency_repository

    def get_currency(self, request: MainHandler):
        code = request.path.split('/')[-1].upper()
        currency = self._currency_repository.find_by_code(code)
        if currency is None:
            return json.dumps({}).encode('utf-8')
        return json.dumps(currency.to_dict()).encode('utf-8')

    def get_currencies(self, request=None):
        currencies = self._currency_repository.find_all()
        return json.dumps([currency.to_dict() for currency in currencies]).encode('utf-8')

    def save_currency(self, request: MainHandler):
        length = int(request.headers.get('Content-Length', 0))
        if not length:
            raise Exception('Content-Length - не задан header')
        content_type = request.headers.get('Content-Type', None)
        if not content_type:
            raise Exception('Content-Type - не задан в header')

        data = request.rfile.read(length).decode('utf-8')
        match content_type:
            case 'application/x-www-form-urlencoded':
                currency = form_to_currency(data)
            case 'application/json':
                currency = json_to_currency(data)
            case _:
                raise Exception(f'Не известный Content-Type - {content_type}')
        return json.dumps(self._currency_repository.save(currency).to_dict()).encode('utf-8')
