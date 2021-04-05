from datetime import datetime, timedelta
import time
import ephem

now = datetime.utcnow()
start_dt = end_dt = datetime(2020, 1, 1)
end_dt = datetime(2039, 12, 31)


print("Start", start_dt)
print("Start", end_dt)

ground_locations = [  # lat, long, metres elevation
  ['-27.36409', '153.08222', 7, "Brisbane"],
]

for location in ground_locations:

  observer = location

  print(" ")
  print(" LOCATION VARIABLES")
  print(" --------------")
  print(" Observer location: " + observer[3] + " (" + observer[0] + ", " + observer[1] + ", " + str(observer[2]) + "m)")

  me = ephem.Observer()
  me.lon = observer[1]
  me.lat = observer[0]
  me.elevation = observer[2]

  events = {}

  # CALCULATING SOLAR EVENTS
  me.date = start_dt
  while me.date.datetime() < end_dt:

    me.pressure= 0
    me.horizon = '-18' #-6=civil twilight, -12=nautical, -18=astronomical

    date = me.date.datetime()
    year = date.year
    month = date.month

    day_rise = me.next_rising(ephem.Sun(), use_center=True).datetime() + timedelta(hours=10)
    day_set = me.next_setting(ephem.Sun(), use_center=True).datetime() + timedelta(hours=10)

    if year not in events:
      events[year] = {}
    if month not in events[year]:
      events[year][month] = {'rise': (day_rise.time().hour, day_rise.time().minute),'set': (day_set.time().hour, day_set.time().minute)}

    if day_rise.time() < datetime(year, month, 1, events[year][month]['rise'][0],events[year][month]['rise'][1],0).time():
      events[year][month]['rise'] = (day_rise.time().hour, day_rise.time().minute)

    if day_set.time() > datetime(year, month, 1, events[year][month]['set'][0],events[year][month]['set'][1],0).time():
      events[year][month]['set'] = (day_set.time().hour, day_set.time().minute)

    me.date = me.date.datetime() + timedelta(days=1)

    # print(date, (day_rise.hour, day_rise.minute), events[year][month]['rise'])
    # print(date, (day_set.hour, day_set.minute), events[year][month]['set'])
    #
    # print()

  #
  # for year in events:
  #   print(year)
  #   for month in events[year]:
  #     print("  ", month, events[year][month]['rise'], "-", events[year][month]['set'])

print(events)
