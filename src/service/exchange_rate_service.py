import json

from src.repository.exchange_rate_repository import ExchangeRateRepository
from src.mapper.exchange_rate_mapper import json_to_exchange_rate
from src.handler import MainHandler
from decimal import Decimal


class ExchangeRateService:
    def __init__(self, exchange_rate_repo: ExchangeRateRepository):
        self._exchange_rate_repo = exchange_rate_repo

    def get_exchange_rate(self, request: MainHandler):
        code = request.path.split('/')[-1].upper()
        exchange_rate = self._exchange_rate_repo.find_by_code(code.upper())
        if exchange_rate is None:
            return json.dumps({}).encode('utf-8')
        return json.dumps(exchange_rate.to_dict()).encode('utf-8')

    def get_exchange_rates(self, request=None):
        exchange_rates = self._exchange_rate_repo.find_all()
        return json.dumps([exchange_rate.to_dict() for exchange_rate in exchange_rates]).encode('utf-8')

    def update_exchange_rate(self, code: str, rate: Decimal):
        self._exchange_rate_repo.update(code.upper(), rate)

    def save_exchange_rate(self, request: MainHandler):
        length = int(request.headers.get('Content-Length', 0))
        if not length:
            raise Exception('Content-Length - не задан header')
        content_type = request.headers.get('Content-Type', None)
        if not content_type:
            raise Exception('Content-Type - не задан в header')

        data = request.rfile.read(length).decode('utf-8')
        if content_type != 'application/json':
            raise Exception(f'Не известный Content-Type - {content_type}')
        exchange_rate = json_to_exchange_rate(data)

        return json.dumps(self._exchange_rate_repo.save(exchange_rate).to_dict()).encode('utf-8')

    def exchange(self):
        pass
