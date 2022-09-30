#  coding: utf-8 
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode("utf-8")
        print ("Got a request of: %s\n" % self.data)
        
        http_request = self.data.splitlines()[0].split()
        request_method = http_request[0]
        path = http_request[1]
        
        if request_method != 'GET':
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed",'utf-8'))
        else:
            self.response = ''
            file_path = os.path.abspath("www") + path
            if (os.path.exists(file_path)):
                if (os.path.isdir(file_path)):
                    if (file_path.endswith("/")):
                        file_path += "index.html"
                        self.handle_file(file_path)
                    else:
                        self.error_301(file_path)
                else:
                    self.handle_file(file_path)
            else:
                self.error_404()
            
            self.request.sendall(bytearray(self.response,'utf-8')) 
    
    def error_301(self, path):
        self.response += ("HTTP/1.1 301 Moved Permanently\n"+
                    "Content-Type: 'text/plain"+"\n\n"+
                    "Location: "+ path + '/\n')

    def error_404(self):
        self.response += ("HTTP/1.1 404 Not Found\r\n")

    def handle_file(self, path):
        if path.endswith("css"):
            content_type = "text/css"
        elif path.endswith("html"):
            content_type = "text/html"
        else:
            self.error_404()
            return
        self.serve(content_type, path)  
   
    def serve(self, content_type, path):
        self.response += ("HTTP/1.1 200 OK\n"+
                    "Content-Type: "+content_type+"\n\n"+
                    open(path).read())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
