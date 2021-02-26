import gc
import webrepl
from network import WLAN, STA_IF, AP_IF
webrepl.start()
gc.collect()
from time import sleep
ap_if = WLAN(AP_IF)
sta_if = WLAN(STA_IF)
STATION_ID = "YOUR_STATION_ID"
PASSWORD = "YOUR_WIFI_PASSWORD"
ip_address = "IP_OF_THE_DEVICE"

def set_ip():
    sta_if.ifconfig((ip_address, "255.255.255.0", "10.0.0.255", "10.0.0.1"))
    sleep(1)
    print("IP: ", ip_address)
    return True


def waiting(cdn):
   sta_if.connect(STATION_ID, PASSWORD)
   count = 0
   while not sta_if.isconnected():
       count = count + 1
       print("Connecting ...", count)
       sleep(1)
       if count >cdn:
          break
       else:
          pass
   if sta_if.isconnected():
       print("Connection Established \n IP INFO:", sta_if.ifconfig())
       ip_change = set_ip()
       while not ip_change:
           pass
   else:
       ap_if.active(True)

def autonet():
       if not sta_if.isconnected():
            if sta_if.active():
                waiting(90)
            else:
                sta_if.active(True)
                waiting(2)
            if not sta_if.isconnected():
                ap_if.active(True)
                print("Station Mode Active \n IP INFO:", ap_if.ifconfig())
            else:
                ap_if.active(False)
       else:
            print("Already connected")

autonet()
