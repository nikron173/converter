import datetime


class ApplicationError(BaseException):
    def __init__(self, message: str, code: int):
        super().__init__()
        self._message = message
        self._code = code
        self._time = datetime.datetime.now()

    @property
    def code(self):
        return self._code

    def to_dict(self):
        return {
            'Error': self._message,
            'StatusCode': self._code,
            'Time': str(self._time)
        }
