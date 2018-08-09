#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import time
from collections import defaultdict
import binascii

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
from panda import Panda

if __name__ == "__main__":
  p = Panda()
  p.set_safety_mode(0x1337)
  print("receiving")
  while True:
    can_recv = p.can_recv()
    for address, _, dat, src  in can_recv:
      print(address, dat, src)

