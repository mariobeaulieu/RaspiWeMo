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

while True:
  if hour_ON == time.localtime().tm_hour and min_ON == time.localtime().tm_min:
    L.on()
    print (str(time.localtime().tm_hour)+"h"+str(time.localtime().tm_min)+"m : WeMo now ON")
  if hour_OFF == time.localtime().tm_hour and min_OFF == time.localtime().tm_min:
    L.off()
    print (str(time.localtime().tm_hour)+"h"+str(time.localtime().tm_min)+"m : WeMo now OFF")
  time.sleep(60)
