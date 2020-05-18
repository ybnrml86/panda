#!/usr/bin/env python3
import time
import struct
from panda import Panda
from hexdump import hexdump
from panda.python.isotp import isotp_send, isotp_recv

if __name__ == "__main__":
  panda = Panda()
  panda.set_safety_mode(Panda.SAFETY_ELM327)
  # 0 - white/grey panda in OBD2, 1 - black panda/comma two + CPv2 in OBD2
  bus = 1
  panda.can_clear(bus)

  # OBD Mode 22 PIDs for Subaru
  # 22 F1 00 SSM ID
  # 22 F1 82 ROM ID
  # 22 F1 89 Version string - only 5 non-essential ecus
  # 22 F1 8E Product code
  # 22 F1 90 VIN - only 7e0
  # 22 F1 97 System String

  # ECU TX addresses for Crosstrek 2018 discovered by selfdrive/car/fw_versions.py --scan
  #ecu_list = [0x735, 0x746, 0x747, 0x752, 0x753, 0x780, 0x783, 0x787, 0x7b0, 0x7c4, 0x7d0, 0x7e0, 0x7e1, 0x7f1]

  # 0x756 responds in accessory mode only
  #ecu_list = [0x756]

  #cmd = b'\x22\x10\x56' # 7d0 volume up
  cmd = b'\x22\x10\x60'

  # set ecu tx addr
  tx_addr = 0x7d0
  rx_addr = tx_addr + 8

  print('0x%x ' % tx_addr + ''.join(r'\x{:02x}'.format(x) for x in cmd))

  while True:
    isotp_send(panda, cmd, tx_addr, bus)
    ret = isotp_recv(panda, rx_addr, bus)
    hexdump(ret)
    time.sleep(1)
    panda.send_heartbeat()
    #break
