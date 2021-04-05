print("\n------------- START OF MAIN.PY --------------")
import time
import ntptime
import camera
import os
import DS3231
from rise_set import *
from config import *

def captureImage():

  speffect = camera.EFFECT_NONE # EFFECT_NONE EFFECT_NEG EFFECT_BW EFFECT_RED EFFECT_GREEN EFFECT_BLUE EFFECT_RETRO
  whitebalance = camera.WB_SUNNY # WB_NONE WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME
  saturation = -1 # -2,2 (default 0). -2 grayscale
  brightness = -1 # -2,2 (default 0). 2 brightness
  contrast = -1 #-2,2 (default 0). 2 highcontrast
  quality = 10 # 10-63 lower number means higher quality

  print(" > Image Capture")
  (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime(time.time())
  timestamp = '{:02d}-{:02d}-{:02d}'.format(hour,minute,second)
  daydir = '{:04d}-{:02d}-{:02d}'.format(year,month,mday)

  if hour > rise_set[year][month]["rise"][0]:
    after_sunrise = True
  elif hour == rise_set[year][month]["rise"][0] and minute >= rise_set[year][month]["rise"][1]:
    after_sunrise = True
  else:
    after_sunrise = False

  if hour < rise_set[year][month]["set"][0]:
    before_sunset = True
  elif hour == rise_set[year][month]["set"][0] and minute <= rise_set[year][month]["set"][1]:
    before_sunset = True
  else:
    before_sunset = False

  daylight = after_sunrise and before_sunset

  print("   > DateTime: " + '{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}'.format(year,month,mday,hour,minute,second))
  print("     > Start at :", '{:02d}:{:02d}'.format(rise_set[year][month]["rise"][0],rise_set[year][month]["rise"][1]))
  print("     > End at :  ", '{:02d}:{:02d}'.format(rise_set[year][month]["set"][0],rise_set[year][month]["set"][1]))
  if daylight:
    print("     > Day Time")
  else:
    print("     > Night Time - Skip")
    return False
  try:
    camera.init(0, format=camera.JPEG, framesize=camera.FRAME_UXGA)
    print("   > Init Camera.")
    time.sleep_ms(2000)
    camera.speffect(speffect)
    camera.whitebalance(whitebalance)
    camera.saturation(saturation)
    camera.brightness(brightness)
    camera.contrast(contrast)
    camera.quality(quality)
    print("   > Setup Camera.")
    time.sleep_ms(2000)
    img = camera.capture()
    print("   > Captured Image.")
    time.sleep_ms(100)
    camera.deinit()
    print("   > DeInit Camera.")
    time.sleep_ms(100)
    if "sd" in os.listdir("/"):
      if daydir not in os.listdir("/sd"):
        os.mkdir("/sd/" + daydir)
      filepath = "/sd/" + daydir + "/" + timestamp + ".jpg"
    else:
      if daydir not in os.listdir("/imgs"):
        os.mkdir("/imgs/" + daydir)
      filepath = "/imgs/" + daydir + "/" + timestamp + ".jpg"
    print("   > Path to save: " + filepath)
    with open(filepath, 'w') as outFile:
      outFile.write(img)
      print("   > Saved.")
  except:
    print("   > EXCEPTION.")

i2c_csl = machine.Pin(2) # ALSO USED BY SD CARD!!!
i2c_sda = machine.Pin(4)
i2c = machine.SoftI2C(scl=i2c_csl, sda=i2c_sda)
ds3231 = DS3231.DS3231(i2c)
print("RTC Module", ds3231.DateTime())
print("Onboard RTC", rtc.datetime())

if wifi.isconnected():

  # UPDATE ONBOARD RTC AND RTC MODULE FROM NTP
  print('\n > Updating RTCs from NTP')
  try:
    ntptime.settime()
    time_seconds = time.time()
    time_seconds += timezone*3600
    (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime(time_seconds)
    rtc.datetime((year, month, mday, 0, hour, minute, second, 0))
    print("   > Onboard RTC updated to local time: ", rtc.datetime())
    ds3231.DateTime(list(rtc.datetime())[0:-1])
    print("   > RTC Module updated to Onboard RTC: ", ds3231.DateTime())
  except:
    print("   > Couldn't update from NTP time.")
    print('   > Updating Onboard RTC from RTC Module instead:', rtc.datetime())
    rtc.datetime(tuple(list(ds3231.DateTime())+[0]))

  # START FTP
  print("\n > ", end="")
  import uftpd

  # START WEBREPL
  print('\n > Starting WebREPL\n   > ', end='')
  import webrepl
  webrepl.start()

else:

  print('\n > Updating Onboard RTC from RTC Module:', rtc.datetime())
  rtc.datetime(tuple(list(ds3231.DateTime())+[0]))

# MOUNT SD CARD
try:
  print('\n > Mounting SD Card')
  global miso, mosi, sck, cs, sd
  miso = machine.Pin(2)
  cs = machine.Pin(13)
  sck = machine.Pin(14)
  mosi = machine.Pin(15)

  sd = machine.SDCard(slot=3, width=1,
    sck=sck,
    mosi=mosi,
    miso=miso,
    cs=cs)
  uos.mount(sd, '/sd')
  print("   > Mounted at /sd/")
except:
  print("   > Couldn't mount")

# MAIN LOOP

while True:

  print("\n > -- SNAPSHOT --")
  captureImage()

  if wifi.isconnected():
    print("\n > Waiting for " + str(period) + " seconds.")
    time.sleep_ms(int(period * 1000))
  else:
    print("\n > Sleeping then restarting in " + str(period) + " seconds.")
    break

print("\n-------------- END OF MAIN.PY ----------------\n")
machine.deepsleep(int(period*1000))
