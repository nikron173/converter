from abc import ABC, abstractmethod
from src.util.connection_pool import ConnectionPool


class Repository(ABC):
    def __init__(self, pool: ConnectionPool):
        self._pool = pool

    @abstractmethod
    def find_by_id(self, obj_id: int):
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def update(self, obj_id: int, obj: object):
        pass

    @abstractmethod
    def delete(self, obj_id: int):
        pass

    @abstractmethod
    def save(self, obj: object):
        pass

    @abstractmethod
    def find_by_code(self, code: str):
        pass
