#!/usr/bin/env python3
import time
import struct
from panda import Panda
from hexdump import hexdump
from panda.python.isotp import isotp_send, isotp_recv

if __name__ == "__main__":
  panda = Panda()
  panda.set_safety_mode(Panda.SAFETY_ELM327)
  panda.can_clear(0)

  # discovered ECU addresses
  # TX    RX
  # 0x735 0x73d
  # 0x746 0x74e
  # 0x753 0x75b
  # 0x756 0x75e
  # 0x780 0x788
  # 0x7b0 0x7b8
  # 0x7c4 0x7cc
  # 0x7e0 0x7e8
  # 0x7f1 0x7f9

  # OBD Mode 22
  # 22 F1 97 System String
  # 22 F1 00 SSMID
  # 22 F1 82 ROMID
  # 22 F1 90 VIN

  # System String
  isotp_send(panda, b"\x22\xf1\x97", 0x735)
  ret = isotp_recv(panda, 0x73d)
  hexdump(ret)
  print("0x73d %s" % "".join(map(chr, ret[3:])))

  # SSMID 
  isotp_send(panda, b"\x22\xf1\x00", 0x735)
  ret = isotp_recv(panda, 0x73d)
  hexdump(ret)
  print("0x73d %s" % "".join(map(chr, ret[3:])))

  # ROMID
  isotp_send(panda, b"\x22\xf1\x82", 0x735)
  ret = isotp_recv(panda, 0x73d)
  hexdump(ret)
  print("0x73d %s" % "".join(map(chr, ret[3:])))

  # VIN from ECU
  isotp_send(panda, b"\x22\xf1\x90", 0x7e0)
  ret = isotp_recv(panda, 0x7e8)
  hexdump(ret)
  print("0x7e8 %s" % "".join(map(chr, ret[3:])))

