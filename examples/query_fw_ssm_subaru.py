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
  # 0x756 0x75e - responds only in accessory mode
  # 0x780 0x788
  # 0x7b0 0x7b8
  # 0x7c4 0x7cc
  # 0x7e0 0x7e8
  # 0x7f1 0x7f9

  # EOBD Mode 22
  # 22 F1 00 SSM ID
  # 22 F1 82 ROM ID
  # 22 F1 89 Version string (2 ecu responses)
  # 22 F1 90 VIN - only 7e0
  # 22 F1 97 System String
  # 22 F1 98 some ecu responses

  bus = 0

  ecu_list = (0x735, 0x746, 0x746, 0x753, 0x780, 0x7b0, 0x7c4, 0x7e0, 0x7f1)
  #ecu_list = (0x735, 0x756)
  cmd_list = (b'\x00', b'\x82', b'\x89', b'\x90', b'\x97')

  #cmd_list = (b'\x90', b'\x91', b'\x92', b'\x93', b'\x94', b'\x95', b'\x96', b'\x97', b'\x98', b'\x99')

  for cmd_byte in cmd_list:
    for tx_addr in ecu_list:
      cmd = b"\x22\xf1" + cmd_byte
      rx_addr = tx_addr + 0x8

      print("0x%x %s" % (tx_addr, cmd))
      isotp_send(panda, cmd, tx_addr, bus)
      ret = isotp_recv(panda, rx_addr, bus)
      hexdump(ret)
      print("0x%x %s" % (rx_addr, "".join(map(chr, ret[3:]))))
