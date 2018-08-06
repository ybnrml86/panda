#!/usr/bin/env python
import sys
import time
from panda import Panda

p = Panda()

if len(sys.argv) > 1 and sys.argv[1] == "on":
  p.set_esp_power(True)
elif len(sys.argv) > 1 and sys.argv[1] == "reset":
  p.set_esp_power(False)
  print "power off"
  time.sleep(0.5)
  p.set_esp_power(True)
  print "power on"
else:
  p.set_esp_power(False)

