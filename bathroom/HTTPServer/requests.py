from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import simplejson
import random

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
        
        print "in post method"
        self._set_headers()
        self.send_response(200)
        self.end_headers()

        # OBS: creates TypeError if the content-length header is not set
        # OBS OBS: getheader('content-length', default value) 
        content_len = int(self.headers.getheader('content-length',0))
        post_body = self.rfile.read(content_len)
        data = simplejson.loads(self.post_body)
        
        """
        self.data_string = self.rfile.read(int(self.headers['content-length']))

        with open("output.json", "w") as outfile:
            simplejson.dump(data, outfile)

        """
        print "{}".format(data)
        f = open("file.txt")
        self.wfile.write(f.read())
        return
        

def run(server_class=HTTPServer, handler_class=S, port=9966):
    server_address = ('129.241.209.166', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

run()