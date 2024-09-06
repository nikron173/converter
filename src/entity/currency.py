class Currency:
    def __init__(self, id: int = None, code: str = None, full_name: str = None, sign: str = None):
        self.__id = id
        self.__code = code
        self.__full_name = full_name
        self.__sign = sign

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, value):
        self.__code = value

    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, value):
        self.__full_name = value

    @property
    def sign(self):
        return self.__sign

    @sign.setter
    def sign(self, value):
        self.__sign = value

    def to_dict(self):
        return {
            'id': self.__id,
            'code': self.__code,
            'full_code': self.__full_name,
            'sign': self.__sign
        }
