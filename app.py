import http.server

from src.util.connection_pool import ConnectionPool
from src.util.init_db import init_db
from src.repository.currency_repository import CurrencyRepository
from src.repository.exchange_rate_repository import ExchangeRateRepository
from src.service.currency_service import CurrencyService
from src.service.exchange_rate_service import ExchangeRateService
from src.router import Router
from src.handler import MainHandler


def main():
    pool = ConnectionPool('database.db', 5)
    init_db(['init.sql', 'data.sql'], pool.get_connection())
    currency_repo = CurrencyRepository(pool)
    exchange_rate_repo = ExchangeRateRepository(pool)
    currency_service = CurrencyService(currency_repo)
    exchange_rate_service = ExchangeRateService(exchange_rate_repo, currency_repo)
    router = Router()
    router.add_route(r'^/currency/(\w+)$',
                     {
                         'GET': currency_service.get_currency
                     }
                     )
    router.add_route(r'^/currencies$',
                     {
                         'POST': currency_service.save_currency,
                         'GET': currency_service.get_currencies
                     }
                     )
    router.add_route(r'^/exchangeRates$',
                     {
                         'GET': exchange_rate_service.get_exchange_rates,
                         'POST': exchange_rate_service.save_exchange_rate
                     }
                     )
    router.add_route(r'^/exchangeRate/(\w+)$',
                     {
                         'GET': exchange_rate_service.get_exchange_rate,
                         'PATCH': exchange_rate_service.update_exchange_rate,
                         'OPTIONS': exchange_rate_service.update_exchange_rate,
                     }
                     )
    router.add_route(r'^/exchange\?[\w\W]+$',
                     {
                         'GET': exchange_rate_service.exchange
                     }
                     )
    MainHandler.set_router(router)
    try:
        server = http.server.HTTPServer(('', 8080), MainHandler)
        print(f'Starting server {server.server_address}...')
        server.serve_forever()
    except Exception as e:
        print(e)
    finally:
        pool.close_all_connection()


if __name__ == '__main__':
    main()
