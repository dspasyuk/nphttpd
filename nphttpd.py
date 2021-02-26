# License: GPL
# GNU GENERAL PUBLIC LICENSE
# Copyright (C) Denis Spasyuk
import socket
from time import sleep
from machine import Pin
from machine import reset
from neopixel import NeoPixel
from network import WLAN, STA_IF
import gc
gc.enable()

class HttServ(object):
    def __init__(self):
        sta_if = WLAN(STA_IF)
        self.ip_address = sta_if.ifconfig()[0]
        self.port = 80  # set your port here
        pin_id = 5
        nparray = 60
        self.conn = None
        self.s = None
        self.np = NeoPixel(Pin(pin_id), nparray)
        self.run_socket()

    def connection(self, html):
        try:
            self.conn.sendall(html)
            sleep(0.2)
        except Exception as exc:
            print("Send Error", exc.args[0])
            pass
        finally:
            self.conn.close()

    def parse_request(self):
        self.ledout = self.request.find("rgb(")
        self.ledoff = self.request.find("OFF")
        if self.ledout > -1:
            color = ((self.request[self.ledout:self.ledout+40]).split("%22")[0]).replace("%20", "")
            #print(eval(color.replace("rgb", "")))
            for i, pixel in enumerate(self.np):
                 self.np[i] = eval(color.replace("rgb", ""))
                 self.np.write()
        if self.ledoff > -1:
            for i, pixel in enumerate(self.np):
                 self.np[i] = (0,0,0)
                 self.np.write()
        self.request = None

    def run_socket(self):
        self.request = None
        html = None
        try:
            with open("index.html", "r") as fhtml:
                html = fhtml.read()
        except OSError:
            pass
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((self.ip_address, self.port))
            self.s.listen(5)
        except Exception as exc:
            print("Address in use, restarting", exc.args[0])
            sleep(2)
            reset()
            pass
        while True:
            try:
                self.conn, addr = self.s.accept()
                for i in str(self.conn).split():
                    print(i)
            except Exception as exc:
                print("Socket Accept Error ", exc.args[0])
                reset()
                pass
            print('Connected by', addr)
            print("FREE MEM:", gc.mem_free())
            gc.collect()
            try:
                self.request = str(self.conn.recv(1024))
            except Exception as exc:
                print("recv -------------", exc.args[0])
                reset()
                pass
            #if not self.request: break
            self.parse_request()
            self.connection(html)
