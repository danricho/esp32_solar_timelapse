# boot.py -- runs on boot-up
print("\n------------- START OF BOOT.PY --------------")
import ntptime
import time
import machine
import network
from config import *

rtc = machine.RTC()
wifi = network.WLAN(network.STA_IF)
miso = machine.Pin(2)
cs = machine.Pin(13)
sck = machine.Pin(14)
mosi = machine.Pin(15)
sd = None

def connect2wifi():

  print("\n > WiFi Scanning", end='')
  wifi.active(True)
  time.sleep_ms(100)
  networks = wifi.scan()
  print(" - Finished")

  for ssid, bssid, channel, rssi, authmode, hidden in sorted(networks, key=lambda x: x[3], reverse=True):

    ssid = ssid.decode('utf-8')
    if ssid in knownSSIDs:
      print(' > Connecting to WiFi (' + ssid + ')')
      print('   > Trying .', end='')
      wifi.connect(ssid, knownSSIDs[ssid])

      for i in range(0,10):
        if not wifi.isconnected():
          time.sleep_ms(500)
          print('.', end='')
        else:
          break

      if not wifi.isconnected():
        wifi.active(False)
        print(' NO LUCK.')
      else:
        print(' SUCCESS.')

        ip, mask, gateway, dns = wifi.ifconfig()
        print('   > IP address: ', ip)
        print('   > Netmask:    ', mask)
        print('   > Gateway:    ', gateway)
        print('   > DNS:        ', dns)

      return

  print(" > No known networks found.")
  wifi.active(False)

def reboot():
  import machine
  machine.reset()

connect2wifi()

print("\n-------------- END OF BOOT.PY ----------------")
