import sqlite3
import time

from src.error.database_error import DatabaseError


class ConnectionPool:
    def __init__(self, database: str, count_connection: int):
        self.__database = database
        self.__count_connection = count_connection
        self.__queue = []
        self.__create_connection_pool()

    def __create_connection(self):
        try:
            connection = Connection(self.__database, self)
            connection.row_factory = sqlite3.Row
            self.__queue.append(connection)
        except Exception as e:
            raise DatabaseError(e)

    def __create_connection_pool(self):
        for _ in range(self.__count_connection):
            self.__create_connection()

    def get_connection(self) -> sqlite3.Connection:
        try:
            return self.__queue.pop()
        except IndexError:
            print('Список коннектов пуст...\nЖдем 5 секунд')
            time.sleep(5)
            self.get_connection()

    def close_connection(self, connection):
        if len(self.__queue) <= self.__count_connection:
            self.__queue.append(connection)
            print(f'Коннект: {connection} освободился и добавился в pool')

    def close_all_connection(self):
        while self.__queue:
            con = self.__queue.pop()
            con.close_connection()
            print(f'Закрытие коннекта: {con}')


class Connection(sqlite3.Connection):
    def __init__(self, database: str, connection_pool: ConnectionPool):
        super().__init__(database)
        self.__pool = connection_pool

    def close(self):
        self.__pool.close_connection(self)

    def close_connection(self):
        super().close()
        print(f'Коннект: {self} закрылся')
