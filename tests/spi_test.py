#!/usr/bin/env python
import time
"""
import spidev

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 500000

while 1:
  to_send = [0,0,0,0] + [0xaa, 0xbb]
  ret = spi.writebytes(to_send)
  print(ret)
  time.sleep(0.01)
"""

import panda

p = panda.Panda("SPI")
while 1:
  #print p.get_version()
  p.serial_write(0, "test")
  time.sleep(0.01)
#p.reset()

