#!/usr/bin/python
from ouimeaux.environment import Environment as E
import time

hour_ON=17
min_ON=45
hour_OFF=22
min_OFF=0

s='WeMo Light Switch'
env=E()
env.start()

print ("Waiting for switch discovery")
t=0
while s not in env.list_switches():
  env.discover()
  t+=1
  print t

print ("Found switch "+s)
L=env.get_switch(s)

status=L.get_state()
action='OFF'
change=1

while True:
  if hour_ON == time.localtime().tm_hour and min_ON == time.localtime().tm_min:
    action='ON'
    change=1
  if hour_OFF == time.localtime().tm_hour and min_OFF == time.localtime().tm_min:
    action='OFF'
    change=1

  error=0
  if action == 'ON' and status == 0:
    try:
      L.on()
      status=1
    except:
      error=1

  if action == 'OFF' and status == 1:
    try:
      L.off()
      status=0
    except:
      error=1

  if error==0:
    if change==1:
      print (str(time.localtime().tm_mon )+"-"+\
             str(time.localtime().tm_mday)+" "+\
             str(time.localtime().tm_hour)+"h"+\
             str(time.localtime().tm_min )+"m : WeMo now "+action)
      change=0
  else:
    print ("Re-acquiring switch... Waiting for switch discovery")
    t=0
    while s not in env.list_switches():
      env.discover()
      t+=1
      print t
    print ("Found switch "+s)
    L=env.get_switch(s)

  time.sleep(60)

