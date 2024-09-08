import json
import urllib.parse
from http.client import NOT_FOUND, BAD_REQUEST
from src.repository.exchange_rate_repository import ExchangeRateRepository
from src.mapper.exchange_rate_mapper import json_to_exchange_rate
from src.handler import MainHandler
from decimal import Decimal, ConversionSyntax
from src.util.parse_query import get_dict_query_url
from src.util.parse_query import get_dict_form
from src.util.parse_query import get_length_and_content_type
from src.error.application_error import ApplicationError


class ExchangeRateService:
    def __init__(self, exchange_rate_repo: ExchangeRateRepository):
        self._exchange_rate_repo = exchange_rate_repo

    def get_exchange_rate(self, request: MainHandler):
        code = request.path.split('/')[-1].upper()
        exchange_rate = self._exchange_rate_repo.find_by_code(code.upper())
        if exchange_rate is None:
            raise ApplicationError(f'Конвертор \'{code}\' не найден', NOT_FOUND)
        return json.dumps(exchange_rate.to_dict()).encode('utf-8')

    def get_exchange_rates(self, request=None):
        exchange_rates = self._exchange_rate_repo.find_all()
        return json.dumps([exchange_rate.to_dict() for exchange_rate in exchange_rates]).encode('utf-8')

    def update_exchange_rate(self, request: MainHandler):
        code = request.path.split('/')[-1].upper()
        exchange_rate = self._exchange_rate_repo.find_by_code(code.upper())
        if exchange_rate is None:
            raise ApplicationError(f'Конвертор \'{code}\' не найден', NOT_FOUND)

        length, content_type = get_length_and_content_type(request.headers)

        if 'application/x-www-form-urlencoded' != content_type:
            raise ApplicationError('Content-Type должен быть в формате \'application/x-www-form-urlencoded\'',
                                   BAD_REQUEST)

        data = request.rfile.read(length).decode('utf-8')
        data_dict = get_dict_form(data)
        rate_str = data_dict.get('rate')

        if rate_str is None or rate_str.isspace():
            raise ApplicationError(f'Не валидный Rate: \'{rate_str}\'', BAD_REQUEST)
        try:
            rate = Decimal(rate_str)
            if rate < 0:
                raise ApplicationError('Rate должен быть положительным числом', BAD_REQUEST)
        except ConversionSyntax:
            raise ApplicationError('Rate должен быть числом', BAD_REQUEST)
        self._exchange_rate_repo.update(exchange_rate.id, rate)
        exchange_rate.rate = rate
        return json.dumps(exchange_rate.to_dict()).encode('utf-8')

    def save_exchange_rate(self, request: MainHandler):
        length, content_type = get_length_and_content_type(request.headers)

        if content_type != 'application/json':
            raise ApplicationError('Content-Type должен быть в формате \'application/json\'',
                                   BAD_REQUEST)

        data = request.rfile.read(length).decode('utf-8')
        exchange_rate = json_to_exchange_rate(data)

        return json.dumps(self._exchange_rate_repo.save(exchange_rate).to_dict()).encode('utf-8')

    def exchange(self, request: MainHandler):
        query = urllib.parse.urlparse(request.path)
        data = get_dict_query_url(query.query)
        base = data.get('from')
        target = data.get('to')
        amount_str = data.get('amount')
        if not (base and target and amount_str):
            raise ApplicationError(f'Не задан один из параметров: from, to, amount',
                                   BAD_REQUEST)
        try:
            amount = Decimal(amount_str)
        except Exception as e:
            raise ApplicationError('Amount должен быть числом', BAD_REQUEST)
        exchange_rate = self._exchange_rate_repo.find_by_code(f'{base}{target}'.upper())
        if not exchange_rate:
            raise ApplicationError(f'Конвертор \'{base}{target}\' не найден', NOT_FOUND)
        converted_amount = (amount * exchange_rate.rate).quantize(Decimal('0.0001'))
        response = exchange_rate.to_dict()
        response['amount'] = str(amount)
        response['convertedAmount'] = str(converted_amount)
        return json.dumps(response).encode('utf-8')
