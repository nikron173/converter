import re
from typing import Set, Dict
from src.error.router_error import RouterError


class Router:

    __allow_methods = {'GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS'}

    def __init__(self):
        self._routes = {}

    def __check_methods(self, methods: Set[str]):
        return len(methods) != 0 and set(methods) <= self.__allow_methods

    def add_route(self, pattern: str, method: Dict[str, object]):
        '''
        Структура router выглядит следующим образом:
            routes = {
                    pattern_path: {'GET': function, 'POST': function},
                    pattern_path: {'GET': function, 'PATCH': function},
                }
        '''
        method_upper = set(m.upper() for m in method.keys())
        if not (self.__check_methods(method_upper) and len(pattern) != 0):
            raise RouterError(f'Not valid route path or methods: {pattern} - {method}')
        if self._routes.get(pattern):
            self._routes[pattern] = {**self._routes[pattern], **method}
            return
        self._routes[pattern] = method

    def get_method_func(self, path: str, method: str):
        for pattern, methods in self._routes.items():
            match = re.match(pattern, path)
            if match:
                if methods.get(method):
                    return methods.get(method)
        return None


