import datetime
import http.client
import json
from http.server import BaseHTTPRequestHandler
from src.router import Router


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
        self.is_router()
        method = self._router.get_method_func(self.path, self.command)
        if not method:
            self.not_found_method(self.path)
        else:
            try:
                response = method(self)
                self.send_response(http.client.OK)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response)))
                self.end_headers()
                self.wfile.write(response)
            except Exception as e:
                print(e)

    def do_POST(self):
        self.is_router()
        method = self._router.get_method_func(self.path, self.command)
        if not method:
            self.not_found_method(self.path)
        else:
            try:
                response = method(self)
                self.send_response(http.client.CREATED)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response)))
                self.end_headers()
                self.wfile.write(response)
            except Exception as e:
                print(e)

    def do_PATCH(self):
        self.is_router()
        method = self._router.get_method_func(self.path, self.command)
        if not method:
            self.not_found_method(self.path)
        else:
            response = method(self)

    def not_found_method(self, path):
        response = json.dumps({"Error": f"path '{path}' not found", "time": str(datetime.datetime.now())}).encode('utf8')
        self.send_response(http.client.NOT_FOUND)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)
