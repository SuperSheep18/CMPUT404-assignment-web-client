#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
import urlparse
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
        if (port == None):
            port = 80
        print "Conecting to:",host, "on", port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((host, port))
            print("Connection succeeded.")

        except Exception as e:
            print "GIGAERROR: ",e

        return s

    def get_code(self, data):
        if (data):
            print "Code:", data.split(" ")[1]
            return int(data.split(" ")[1])
        else:
            return None

    def get_headers(self, path, host, args=None):
        finalMessage = 'POST '+path+' HTTP/1.1\r\nHost: '+host+'\r\n'
        if (args):
            stuff = urllib.urlencode(args)
            finalMessage += 'content-type: application/json\r\n'
            finalMessage += 'content-length: '+str(len(stuff))+'\r\n\r\n'
            finalMessage += stuff+'\r\n'

        finalMessage += '\r\n'
        return finalMessage

    def get_body(self, data):
        bodyExists = len(data.split("\r\n\r\n")) > 1
        if bodyExists:
            return data.split("\r\n\r\n")[1]
        else:
            return data

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        code = 500
        body = ""

        parsed = urlparse.urlparse(url)

        # Figure out the Port.
        thePort = parsed.port

        # Figure out the URL
        theHost = parsed.netloc.split(":")[0]

        # Connect to Server and send the GET
        s = self.connect(theHost, thePort)
        s.send('GET '+parsed.path+' HTTP/1.1\r\nHost: '+theHost+'\r\n\r\n')

        # Receive the data.
        data = self.recvall(s)
        s.close()

        # Print result to standard out.
        sys.stdout.write('Received Response: '+repr(data))

        # Update the code and body respectively.
        code = self.get_code(data)
        body = self.get_body(data)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        parsed = urlparse.urlparse(url)

        # Figure out the Port.
        thePort = parsed.port

        # Figure out the URL
        theHost = parsed.netloc.split(":")[0]

        # Connect to Server and send the GET
        s = self.connect(theHost, thePort)
        s.send(self.get_headers(parsed.path, theHost, args))

        # Receive the data.
        data = self.recvall(s)
        s.close()

        # Print result to standard out.
        sys.stdout.write('Received Response: '+repr(data))

        # Update the code and body respectively.
        code = self.get_code(data)
        body = self.get_body(data)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   
        
    
    
