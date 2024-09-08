from typing import List
from decimal import Decimal
from http.client import BAD_REQUEST, BAD_GATEWAY
from src.repository.repository import Repository
from src.entity.exchange_rate import ExchangeRate
from src.mapper.exchange_rate_mapper import object_to_exchange_rate
from sqlite3.dbapi2 import DatabaseError as db3
from src.error.application_error import ApplicationError


class ExchangeRateRepository(Repository):
    def find_by_code(self, code: str):
        select_by_code = '''
        SELECT e.id as e_id, e.rate as e_rate,
            b.id as b_id, b.code as b_code, b.full_name as b_full_name, b.sign as b_sign,
            t.id as t_id, t.code as t_code, t.full_name as t_full_name, t.sign as t_sign,
            b.code || t.code AS full_code
         FROM exchange_rates e 
            JOIN currencies b ON b.id = e.base_currency_id
            JOIN currencies t ON t.id = e.target_currency_id
         WHERE full_code = :code
         UNION
         SELECT e.id as e_id, 1/e.rate,
            t.id, t.code, t.full_name, t.sign,
            b.id, b.code, b.full_name, b.sign,
            t.code || b.code AS full_code
         FROM exchange_rates e 
            JOIN currencies b ON b.id = e.base_currency_id
            JOIN currencies t ON t.id = e.target_currency_id
         WHERE full_code = :code
         '''
        con = self._pool.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute(select_by_code, {'code': code})
            obj = cursor.fetchone()
            if obj is None:
                return None
            return object_to_exchange_rate(**obj)
        except db3 as e:
            raise ApplicationError(str(e), BAD_GATEWAY)
        finally:
            if con:
                con.close()

    def find_by_id(self, object_id: int) -> None | ExchangeRate:
        select_by_id = '''
        SELECT e.id, e.rate as rate,
            b.id, b.code, b.full_name, b.sign,
            t.id, t.code, t.full_name, t.sign
         FROM exchange_rates e 
            JOIN currencies b ON b.id = e.base_currency_id
            JOIN currencies t ON t.id = e.target_currency_id
         WHERE e.id = :id
        '''
        con = self._pool.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute(select_by_id, {'id': object_id})
            obj = cursor.fetchone()
            if obj is None:
                return None
            return object_to_exchange_rate(**obj)
        except db3 as e:
            raise ApplicationError(str(e), BAD_GATEWAY)
        finally:
            if con:
                con.close()

    def find_all(self) -> List[ExchangeRate]:
        select_all = '''
        SELECT e.id as e_id, e.rate as e_rate,
            b.id as b_id, b.code as b_code, b.full_name as b_full_name, b.sign as b_sign,
            t.id as t_id, t.code as t_code, t.full_name as t_full_name, t.sign as t_sign
         FROM exchange_rates e 
            JOIN currencies b ON b.id = e.base_currency_id
            JOIN currencies t ON t.id = e.target_currency_id
        '''
        con = self._pool.get_connection()
        exchange_rates = []
        try:
            cursor = con.cursor()
            cursor.execute(select_all)
            for obj in cursor:
                exchange_rates.append(object_to_exchange_rate(**obj))
        except db3 as e:
            raise ApplicationError(str(e), BAD_GATEWAY)
        finally:
            if con:
                con.close()
        return exchange_rates

    def update(self, id: int, rate: Decimal) -> None:
        update_currency = '''UPDATE exchange_rates SET rate = :rate
         WHERE id = :id
         '''
        con = self._pool.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute(update_currency,
                           {
                               'rate': str(rate.quantize(Decimal('0.0001'))),
                               'id': id}
                           )
        except db3 as e:
            raise ApplicationError(str(e), BAD_GATEWAY)
        finally:
            if con:
                con.close()

    def delete(self, obj_id: int) -> None:
        delete_by_id = 'DELETE FROM exchange_rates WHERE id = :id'
        con = self._pool.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute(delete_by_id, {'id': obj_id})
        except db3 as e:
            raise ApplicationError(str(e), BAD_GATEWAY)
        finally:
            if con:
                con.close()

    def save(self, obj: ExchangeRate) -> ExchangeRate:
        save_exchange_rate = '''INSERT INTO exchange_rates 
        (base_currency_id, target_currency_id, rate) 
        VALUES (:base, :target, :rate)'''
        con = self._pool.get_connection()
        try:
            print(obj.to_dict())
            cursor = con.cursor()
            cursor.execute(save_exchange_rate,
                           {'base': obj.base.id,
                            'target': obj.target.id,
                            'rate': obj.rate
                            }
                           )
            obj.id = cursor.lastrowid
            return obj
        except db3 as e:
            message = str(e)
            if e.sqlite_errorcode == 2067:
                message = f'Конвертер \'{obj.base.code.upper()}{obj.target.code.upper()}\' уже есть в базе данных'
            raise ApplicationError(message, BAD_REQUEST)
        finally:
            if con:
                con.close()
