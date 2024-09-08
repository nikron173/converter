import datetime
from http.client import BAD_GATEWAY, OK, CREATED, NOT_FOUND
import json
from http.server import BaseHTTPRequestHandler
from src.router import Router
from src.error.application_error import ApplicationError


class MainHandler(BaseHTTPRequestHandler):
    _router = None

    def __init__(self, request, client_address, server_class):
        self.server_class = server_class
        super().__init__(request, client_address, server_class)

    @classmethod
    def set_router(cls, router: Router):
        cls._router = router

    def is_router(self):
        if self._router is None:
            raise Exception(f'With {self.__class__.__name__} router is None')

    def do_GET(self):
        self.response(OK)

    def do_POST(self):
        self.response(CREATED)

    def do_PATCH(self):
        self.response(OK)

    def not_found_method(self, path):
        response = json.dumps({"Error": f"path '{path}' not found", "time": str(datetime.datetime.now())}).encode(
            'utf8')
        self.send_response(NOT_FOUND)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def response_wrapper(self, code: int, response: bytes):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def response(self, code):
        self.is_router()
        method = self._router.get_method_func(self.path, self.command)
        if not method:
            self.not_found_method(self.path)
        else:
            try:
                response = method(self)
                self.response_wrapper(code, response)
            except ApplicationError as e:
                self.response_wrapper(e.code, json.dumps(e.to_dict()).encode('utf-8'))
            except Exception as e:
                response = {
                    'Error': str(e),
                    'Time': str(datetime.datetime.now())
                }
                self.response_wrapper(BAD_GATEWAY, json.dumps(response).encode('utf-8'))
