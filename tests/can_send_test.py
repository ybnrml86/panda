#!/usr/bin/env python
import panda
import time
p = panda.Panda()
p.set_safety_mode(0x1337)

for i in range(0, 0x100):
  print("send")
  p.can_send(0x1aa, chr(i), 0)
  time.sleep(0.05)
  print(p.can_recv())

