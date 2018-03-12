#!/usr/bin/python
from ouimeaux.environment import Environment as E
from astral import Astral
import time
import datetime
import sys

a=Astral()
a.solar_depression='civil'
city=a['Ottawa']
today=0


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

while True:

  change=0
  time_now=datetime.datetime.now().replace(tzinfo=None)

  if time_now.date() != today:
     today = time_now.date()
     dusk = city.sun()['dusk'].replace(tzinfo=None)
     time_ON = dusk
     time_OFF= time_ON + datetime.timedelta(hours=3)
     print s," will turn ON at ",time_ON, " and OFF at ",time_OFF

  if time_ON < time_now and time_now < time_OFF:
    if status == 0:
      action='ON'
      change=1
  else:
    if status == 1:
      action='OFF'
      change=1

  error=0
  if change == 1:
    if status == 0:
      try:
        L.on()
        status=1
      except:
        error=1
        print "Eror: ", sys.exc_info()[0]
    else:
      try:
        L.off()
        status=0
      except:
        error=1
        print "Eror: ", sys.exc_info()[0]

    if error==0:
      print (str(time.localtime().tm_mon )+"-"+\
             str(time.localtime().tm_mday)+" "+\
             str(time.localtime().tm_hour)+"h"+\
             str(time.localtime().tm_min )+"m : WeMo now "+action)
    else:
      print ("Re-acquiring switch... Waiting for switch discovery")
      t=0
      while s not in env.list_switches():
        env.discover()
        t+=1
        print t
      print ("Found switch "+s)
      L=env.get_switch(s)
      status=L.get_state()

  time.sleep(60)

