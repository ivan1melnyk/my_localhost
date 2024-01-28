from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import socket
import json


UDP_IP = '127.0.0.1'
UDP_PORT = 5000


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)

        match pr_url.path:
            case '/':
                self.send_html_file('public/index.html')

            case  '/contact':
                self.send_html_file('public/message.html')
            case '/public/style.css':
                self.send_static()
            case '/public/logo.png':
                self.send_static()
            case '/public/user_cat.png':
                self.send_static()
            case _:
                self.send_html_file('public/error.html', 404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.unquote(post_data)

        # Parse the form data into a dictionary
        form_data = {}
        for item in parsed_data.split('&'):
            key, value = item.split('=')
            form_data[key] = value

        # Send data to server
        self.run_client(UDP_IP, UDP_PORT, form_data)

        # Send a redirect response
        self.send_response(302)
        self.send_header("Location", '/contact')
        self.end_headers()

    def send_html_file(self, filename, status=200):
        ext = filename.split(".")[1]
        print(filename)
        self.send_response(status)
        self.send_header('Content-type', f'text/{ext}')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def run_client(self, ip, port, MESSAGE):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server = ip, port
        print(MESSAGE)
        print(json.dumps(MESSAGE))

        data = json.dumps(MESSAGE).encode('utf-8')
        sock.sendto(data, server)
        print(f'Send data: {data.decode()} to server: {server}')
        response, address = sock.recvfrom(1024)
        print(f'Response data: {response.decode()} from address: {address}')
        sock.close()


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()
