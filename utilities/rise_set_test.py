from rise_set import *

year = 2021
month = 5

for hour in range(0,24):
  for minute in range(0,60):
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
