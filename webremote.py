#!/usr/bin/env python2

print("Welcome to WebRemote...")

html = """<html>
<head>
<title>WebRemote</title>
</head>
<body>
test
</body>
</html>"""

import BaseHTTPServer
import uinput
import threading
import urlparse
import os
import base64
import hashlib
import struct

lock = threading.Lock()

events = (
    uinput.REL_X,
    uinput.REL_Y,
    uinput.BTN_LEFT,
    uinput.BTN_RIGHT
    )
device = uinput.Device(events)

class WebRemoteHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def WS_upgrade(self):
        print(self.headers)
        key = self.headers.get("Sec-WebSocket-Key","")
        accept = base64.b64encode(hashlib.sha1(key+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11").digest())
        print("sending header")
        self.wfile.write(('''
HTTP/1.1 101 Switching Protocols\r
Upgrade: WebSocket\r
Connection: Upgrade\r
WebSocket-Protocol: protocoluinput\r
Sec-WebSocket-Accept: %s\r
''' % accept).strip() + '\r\n\r\n');
        self.wfile.flush()
        
    def WS_unpack(self):
        data = struct.unpack('!B',self.rfile.read(1))[0]
        flags = data>>4
        if (flags != 8):
            return None
        op = data % 16
        if (op != 1):
            return None
        data = struct.unpack('!B',self.rfile.read(1))[0]
        mask = data>>7
        length = data % 128
        if length >=126:
            return None
        '''if length == 127:
            length = length * 18446744073709551616 + struct.unpack('!Q',self.rfile.read(8))[0]
        if length == 126:
            length = length * 65536 + struct.unpack('!H',self.rfile.read(2))[0]
        print("flags, op, mask, length: %i %i %i %i" % (flags, op, mask, length))'''
        if mask == 1:
            maskkey = bytearray(self.rfile.read(4))
            '''print("maskkey: %s" % base64.b16encode(maskkey))'''
        payload = bytearray(self.rfile.read(length))
        if mask == 1:
            for i in range(len(payload)):
                payload[i] = payload[i] ^ maskkey[i%4]
        return payload
        
    def WS_pack(self, data):
        if (len(data)>100):
            return
        self.wfile.write(struct.pack('!B', (8<<4) | 1))
        self.wfile.write(struct.pack('!B', (0<<7) | len(data)))
        self.wfile.write(bytearray(data))
        print("sending: %s" % data)
        self.wfile.flush()

    def do_WS(self):
        "asdf"

    def do_GET(self):
        self.close_connection = 1
        p = self.path.split("/")
        print("cmd=%s" % p[1])
        if p[1] == "ws":
            self.WS_upgrade()
            print("doing...")
            while (1==1):
                data = self.WS_unpack()
                print("payload: %s" % data)
                self.WS_pack('OK\n')
            print("done...")
        elif p[1] == "":
            f = open('site.html', 'r')
            html = f.read()
            f.close()
            print("Send html")
            self.send_response(200, "OK")
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html)
        elif p[1] == "jquery-1.9.1.min.js":
            f = open("jquery-1.9.1.min.js", "r")
            js = f.read()
            f.close()
            print("Send jquery")
            self.send_response(200, "OK")
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(js)
        elif p[1] == "jquery.event.move.js":
            f = open("jquery.event.move.js", "r")
            js = f.read()
            f.close()
            print("Send jqueryeventmove")
            self.send_response(200, "OK")
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(js)
        elif p[1] == "move" and len(p) == 4:
            try:
                x = int(p[2])
                y = int(p[3])
                print("Move (%i,%i)" % (x,y))
                lock.acquire()
                device.emit(uinput.REL_X, x, syn=False)
                device.emit(uinput.REL_Y, y)
                lock.release()
                self.send_response(204, "OK")
                self.send_header("Content-type", "text/html")
                self.end_headers()
            except ValueError:
                self.send_response(404)
                self.end_headers()
        elif p[1] == "btn" and len(p) == 3:
            if p[2] == "BTN_LEFT":
                lock.acquire()
                device.emit(uinput.BTN_LEFT, 1)
                device.emit(uinput.BTN_LEFT, 0)
                lock.release()
                self.send_response(204,"OK")
                self.send_header("Content-type", "text/html")
                self.end_headers()
            elif p[2] == "BTN_LEFT_DOUBLE":
                lock.acquire()
                device.emit(uinput.BTN_LEFT, 1)
                device.emit(uinput.BTN_LEFT, 0)
                device.emit(uinput.BTN_LEFT, 1)
                device.emit(uinput.BTN_LEFT, 0)
                lock.release()
                self.send_response(204,"OK")
                self.send_header("Content-type", "text/html")
                self.end_headers()
            elif p[2] == "BTN_LEFT_DOWN":
                lock.acquire()
                device.emit(uinput.BTN_LEFT, 1)
                lock.release()
                self.send_response(204,"OK")
                self.send_header("Content-type", "text/html")
                self.end_headers()
            elif p[2] == "BTN_LEFT_UP":
                lock.acquire()
                device.emit(uinput.BTN_LEFT, 0)
                lock.release()
                self.send_response(204,"OK")
                self.send_header("Content-type", "text/html")
                self.end_headers()
            elif p[2] == "BTN_RIGHT":
                lock.acquire()
                device.emit(uinput.BTN_RIGHT, 1)
                device.emit(uinput.BTN_RIGHT, 0)
                lock.release()
                self.send_response(204,"OK")
                self.send_header("Content-type", "text/html")
                self.end_headers()
            elif p[2] == "BTN_VT2":
                lock.acquire()
                os.system("chvt 2");
                lock.release()
                self.send_response(204,"OK")
                self.send_header("Content-type", "text/html")
                self.end_headers()
            elif p[2] == "BTN_VT3":
                lock.acquire()
                os.system("chvt 3");
                lock.release()
                self.send_response(204,"OK")
                self.send_header("Content-type", "text/html")
                self.end_headers()
            elif p[2] == "BTN_VT4":
                lock.acquire()
                os.system("chvt 4");
                lock.release()
                self.send_response(204,"OK")
                self.send_header("Content-type", "text/html")
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
        
http = BaseHTTPServer.HTTPServer(("0.0.0.0", 8880), WebRemoteHandler)
print 'Starting server, use <Ctrl-C> to stop'
http.serve_forever()

