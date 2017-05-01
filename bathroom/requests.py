from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import random
import os

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', '')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        f = open("index.html", "r")
        self.wfile.write(f.read())

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):

        print ("in post method")
        self._set_headers()
        self.send_response(200)
        self.end_headers()

        # OBS: creates TypeError if the content-length header is not set
        # OBS OBS: getheader('content-length', default value)
        content_len = int(self.headers.getheader('content-length',0))
        self.post_body = self.rfile.read(content_len)
        data = json.loads(self.post_body)

        users = get_users(data)
        # self.data_string = self.rfile.read(int(self.headers['content-length']))

        for user in users:
            file_name = user +".json"
            file_ = open(os.path.join("users", file_name), 'w+')
            file_.write(json.dumps(users[user]))
            file_.close()

        

        # with open("output.json", "w") as outfile:
        #     json.dump(data, outfile)

        # Contains the output stream for writing a response back to the client.
        # Proper adherence to the HTTP protocol must be used when
        #  writing to this stream.
        
        return


def run(server_class=HTTPServer, handler_class=S, port=9966):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

def get_users(data):
    users = {}

    for alarm in data:
        if users.get(alarm["userId"]):
            users.get(alarm["userId"]).append(alarm)
        else:
            users[alarm["userId"]] = [alarm]
        
    return users

run()