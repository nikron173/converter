from decimal import Decimal

from src.entity.currency import Currency


class ExchangeRate:
    def __init__(self, id: int = None, base: Currency = None, target: Currency = None, rate: Decimal = None):
        self.__id = id
        self.__base = base
        self.__target = target
        self.__rate = rate

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def base(self):
        return self.__base

    @base.setter
    def base(self, value):
        self.__base = value

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        self.__target = value

    @property
    def rate(self):
        return self.__rate

    @rate.setter
    def rate(self, value):
        self.__rate = value

    def to_dict(self):
        return {
            'id': self.__id,
            'baseCurrency': self.__base.to_dict(),
            'targetCurrency': self.__target.to_dict(),
            'rate': str(self.__rate.quantize(Decimal('0.0001')))
        }
