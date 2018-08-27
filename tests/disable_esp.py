#!/usr/bin/env python
import sys
import time
from panda import Panda

p = Panda(claim=False)

if len(sys.argv) > 1 and sys.argv[1] == "on":
  p.set_esp_power(True)
elif len(sys.argv) > 1 and sys.argv[1] == "reset":
  p.set_esp_power(False)
  print "power off"
  time.sleep(0.1)
  p.set_esp_power(True)
  print "power on"
elif len(sys.argv) > 1 and sys.argv[1] == "boot":
  p.set_esp_power(False)
  print "power off"
  time.sleep(0.1)
  p.set_esp_power(2)
  print "boot on"
else:
  p.set_esp_power(False)

