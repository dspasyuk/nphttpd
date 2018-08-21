# License: GPL
# GNU GENERAL PUBLIC LICENSE
# Copyright (C) Denis Spasyuk
import socket
import time
from machine import Pin
from machine import reset
from neopixel import NeoPixel

IP_ADDRESS = "192.168.0.15" #set your ip here


def zero():
    ledred = -1
    ledgreen = -1
    ledblue = -1
    ledwhite = -1
    ledpurple = -1
    ledyellow = -1
    ledsblue = -1
    ledtur = -1
    ledoff = -1


def httserv():
    try:
        fhtml = open("index.html", "r")
        html = fhtml.read()
        fhtml.close()
    except OSError:
        pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((IP_ADDRESS, 80))
        s.listen(5)
    except Exception as exc:
        print("Address in use, restarting", exc.args[0])
        time.sleep(2)
        reset()
        pass
    np = NeoPixel(Pin(5), 60)
    vvv = 255
    while True:
        zero()
        try:
            conn, addr = s.accept()
        except Exception as exc:
            print("Socket Accept Error ", exc.args[0])
            reset()
            pass
        try:
            request = conn.recv(1024)
        except Exception as exc:
            print("recv -------------", exc.args[0])
            reset()
            pass
        request = str(request)
        ledred = request.find("RED")
        ledgreen = request.find("GREEN")
        ledblue = request.find("BLUE")
        ledwhite = request.find("WHITE")
        ledpurple = request.find("PURPLE")
        ledyellow = request.find("YELLOW")
        ledsblue = request.find("SKYBL-UE")
        ledtur = request.find("TURQUOISE")
        ledoff = request.find("OFF")
        if ledred > -1:
            for i, pixel in enumerate(np):
                np[i] = (vvv, 0, 0)
                np.write()
        if ledgreen > -1:
            for i, pixel in enumerate(np):
                np[i] = (0, vvv, 0)
                np.write()
        if ledblue > -1:
            for i, pixel in enumerate(np):
                np[i] = (0, 0, vvv)
                np.write()
        if ledsblue > -1:
            for i, pixel in enumerate(np):
                np[i] = (135, 206, 235)
                np.write()
        if ledwhite > -1:
            for i, pixel in enumerate(np):
                np[i] = (vvv, vvv, vvv)
                np.write()
        if ledoff > -1:
            for i, pixel in enumerate(np):
                np[i] = (0, 0, 0)
                np.write()
        if ledpurple > -1:
            for i, pixel in enumerate(np):
                np[i] = (vvv, 0, vvv)
                np.write()
        if ledyellow > -1:
            for i, pixel in enumerate(np):
                np[i] = (vvv, vvv, 0)
                np.write()
        if ledtur > -1:
            for i, pixel in enumerate(np):
                np[i] = (64, 224, 208)
                np.write()
        zero()
        response = html
        request = None
        try:
            conn.sendall(response)
            time.sleep(0.2)
        except Exception as exc:
            print("Send Error", exc.args[0])
            pass
        finally:
            conn.close()
