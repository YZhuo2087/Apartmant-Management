import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler
from http_handler import BaseServer


class CustomHandler(BaseServer, SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/static/'):
            SimpleHTTPRequestHandler.do_GET(self)
        else:
            BaseServer.do_GET(self)


def start_http_server():
    logging.basicConfig(level=logging.INFO)
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, CustomHandler)
    logging.info('Starting httpd...\n')
    logging.info('Server start at: http://localhost:8080 \n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == "__main__":
    start_http_server()
