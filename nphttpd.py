# License: GPL
# GNU GENERAL PUBLIC LICENSE
# Copyright (C) Denis Spasyuk
import socket
import time
from machine import Pin
from machine import reset
from neopixel import NeoPixel


class HttServ(object):
    def __init__(self):
        self.ip_address = "192.168.0.12"  # set your ip here
        self.port = 80  # set your port here
        pin_id = 5
        nparray = 60
        self.conn = None
        self.s = None
        self.np = NeoPixel(Pin(pin_id), nparray)
        self.run_socket()

    def zero(self):
        self.ledred = -1
        self.ledgreen = -1
        self.ledblue = -1
        self.ledwhite = -1
        self.ledpurple = -1
        self.ledyellow = -1
        self.ledsblue = -1
        self.ledtur = -1
        self.ledoff = -1

    def connection(self, html):
        try:
            self.conn.sendall(html)
            time.sleep(0.2)
        except Exception as exc:
            print("Send Error", exc.args[0])
            pass
        finally:
            self.conn.close()
            #self.s.close()
            self.zero()

    def parse_request(self):
        vvv = 255
        self.ledred = self.request.find("RED")
        self.ledgreen = self.request.find("GREEN")
        self.ledblue = self.request.find("BLUE")
        self.ledwhite = self.request.find("WHITE")
        self.ledpurple = self.request.find("PURPLE")
        self.ledyellow = self.request.find("YELLOW")
        self.ledsblue = self.request.find("SKYBL-UE")
        self.ledtur = self.request.find("TURQUOISE")
        self.ledoff = self.request.find("OFF")
        if self.ledred > -1:
            for i, pixel in enumerate(self.np):
                self.np[i] = (vvv, 0, 0)
                self.np.write()
        if self.ledgreen > -1:
            for i, pixel in enumerate(self.np):
                self.np[i] = (0, vvv, 0)
                self.np.write()
        if self.ledblue > -1:
            for i, pixel in enumerate(self.np):
                self.np[i] = (0, 0, vvv)
                self.np.write()
        if self.ledsblue > -1:
            for i, pixel in enumerate(self.np):
                self.np[i] = (135, 206, 235)
                self.np.write()
        if self.ledwhite > -1:
            for i, pixel in enumerate(self.np):
                self.np[i] = (vvv, vvv, vvv)
                self.np.write()
        if self.ledoff > -1:
            for i, pixel in enumerate(self.np):
                self.np[i] = (0, 0, 0)
                self.np.write()
        if self.ledpurple > -1:
            for i, pixel in enumerate(self.np):
                self.np[i] = (vvv, 0, vvv)
                self.np.write()
        if self.ledyellow > -1:
            for i, pixel in enumerate(self.np):
                self.np[i] = (vvv, vvv, 0)
                self.np.write()
        if self.ledtur > -1:
            for i, pixel in enumerate(self.np):
                self.np[i] = (64, 224, 208)
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
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((self.ip_address, self.port))
            self.s.listen(5)
        except Exception as exc:
            print("Address in use, restarting", exc.args[0])
            time.sleep(2)
            reset()
            pass
        while True:
            self.zero()
            try:
                self.conn, addr = self.s.accept()
            except Exception as exc:
                print("Socket Accept Error ", exc.args[0])
                reset()
                pass
            print('Connected by', addr)
            try:
                self.request = str(self.conn.recv(1024))
            except Exception as exc:
                print("recv -------------", exc.args[0])
                reset()
                pass
            self.parse_request()
            self.connection(html)
