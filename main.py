import uuid
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

HOST = "localhost"
PORT = 8000


class http_server(BaseHTTPRequestHandler):
    '''This class handles every request which from the user'''

    def do_GET(self):
        print(self.path)
        if (self.path.endswith("html")):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            index_location = './index.html'
            file_content = open(index_location).read()
            self.wfile.write(bytes(file_content, 'utf-8'))

        elif (self.path.endswith("json")):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            dictionary_location = './dictionary.json'
            file_content = open(dictionary_location).read()
            self.wfile.write(bytes(file_content, 'utf-8'))

        elif (self.path.endswith("uuid")):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            content = {
                "uuid": str(uuid.uuid4())
            }
            self.wfile.write(bytes(json.dumps(content), 'utf-8'))

        # for solving status and delay problem here firstly I am storing the path to src variable
        src = self.path
        if src.split('/')[-2] == 'status':
            code = int(src.split('/')[-1])

            if code >= 600:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                response = f'ERROR: 404'
                self.wfile.write(bytes(response, 'utf-8'))

            else:
                self.send_response(code)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                response = f'responded: {code}'
                self.wfile.write(bytes(response, 'utf-8'))

        elif (src.split('/')[-2] == 'delay'):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            delay_time = int(src.split('/')[-1])
            time.sleep(delay_time)
            response = f'responded after {delay_time}s'
            self.wfile.write(bytes(response, 'utf-8'))


server = HTTPServer((HOST, PORT), http_server)

print("Server now running...")
server.serve_forever()
