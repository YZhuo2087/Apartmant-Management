from http.server import BaseHTTPRequestHandler
import logging
import re
from routes import ROUTE_TO_HANDLER


class BaseServer(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _serve_template(self, template_name, context):
        try:
            with open(f'templates/{template_name}', 'r') as file:
                template = file.read()
            for key, value in context.items():
                template = template.replace(f'{{{{ {key} }}}}', value)
            self.wfile.write(bytes(template, 'utf-8'))
        except FileNotFoundError:
            self.send_error(404, "Template Not Found")
        except Exception as e:
            logging.error(f"Error serving template: {e}")
            self.send_error(500, "Internal Server Error")

    def do_GET(self):
        logging.info("GET request,\nPath: %s\n", str(self.path))

        for pattern, callback in ROUTE_TO_HANDLER.items():
            if (m := re.fullmatch(pattern, self.path)):
                logging.info("Found matched handler: %s", pattern)
                callback(self, m.groupdict())
                return
        self.send_error(404, "Not Found")

    def do_POST(self):
        logging.info("POST request,\nPath: %s\n", str(self.path))

        for pattern, callback in ROUTE_TO_HANDLER.items():
            if (m := re.fullmatch(pattern, self.path)):
                logging.info("Found matched handler: %s", pattern)
                callback(self, m.groupdict())
                return
        self.send_error(404, "Not Found")
