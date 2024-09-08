from http.client import BAD_REQUEST, BAD_GATEWAY

from src.repository.repository import Repository
from src.entity.currency import Currency
from src.mapper.currency_mapper import object_to_currency
from typing import List
from sqlite3 import DatabaseError as db3
from src.error.application_error import ApplicationError


class CurrencyRepository(Repository):
    def find_by_code(self, code: str):
        select_by_code = 'SELECT id, code, full_name, sign FROM currencies WHERE code = :code'
        con = self._pool.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute(select_by_code, {'code': code})
            obj = cursor.fetchone()
            if obj is None:
                return None
            return object_to_currency(**obj)
        except db3 as e:
            raise ApplicationError(str(e), BAD_GATEWAY)
        finally:
            if con:
                con.close()

    def find_by_id(self, object_id: int) -> None | Currency:
        select_by_id = 'SELECT id, code, full_name, sign FROM currencies WHERE id = :id'
        con = self._pool.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute(select_by_id, {'id': object_id})
            obj = cursor.fetchone()
            if obj is None:
                return None
            return object_to_currency(**obj)
        except db3 as e:
            raise ApplicationError(str(e), BAD_GATEWAY)
        finally:
            if con:
                con.close()

    def find_all(self) -> List[Currency]:
        select_all = 'SELECT id, code, full_name, sign FROM currencies'
        con = self._pool.get_connection()
        currencies = []
        try:
            cursor = con.cursor()
            cursor.execute(select_all)
            for obj in cursor:
                currencies.append(object_to_currency(**obj))
        except db3 as e:
            raise ApplicationError(str(e), BAD_GATEWAY)
        finally:
            if con:
                con.close()
        return currencies

    def update(self, obj_id: int, obj: Currency) -> None:
        update_currency = 'UPDATE currencies SET code = :code, full_name = :full_name, sign = :sign WHERE id = :id'
        con = self._pool.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute(update_currency,
                           {'code': obj.code,
                            'full_name': obj.full_name,
                            'sign': obj.sign,
                            'id': obj_id}
                           )
        except db3 as e:
            raise ApplicationError(str(e), BAD_GATEWAY)
        finally:
            if con:
                con.close()

    def delete(self, obj_id: int) -> None:
        delete_by_id = 'DELETE FROM currencies WHERE id = :id'
        con = self._pool.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute(delete_by_id, {'id': obj_id})
        except db3 as e:
            raise ApplicationError(str(e), BAD_GATEWAY)
        finally:
            if con:
                con.close()

    def save(self, obj: Currency) -> Currency:
        save_currency = 'INSERT INTO currencies (code, full_name, sign) VALUES (:code, :full_name, :sign)'
        con = self._pool.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute(save_currency,
                           {'code': obj.code,
                            'full_name': obj.full_name,
                            'sign': obj.sign}
                           )
            obj.id = cursor.lastrowid
            return obj
        except db3 as e:
            message = str(e)
            if e.sqlite_errorcode == 2067:
                message = f'Валюта \'{obj.code}\' уже есть в базе данных'
            raise ApplicationError(message, BAD_REQUEST)
        finally:
            if con:
                con.close()
