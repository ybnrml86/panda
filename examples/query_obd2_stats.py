#!/usr/bin/env python3
import time
import struct
from panda import Panda
from hexdump import hexdump
from panda.python.isotp import isotp_send, isotp_recv

# OBD Mode 22 info PIDs for Subaru
#
# 22 F1 00 SSM ID
# 22 F1 82 ROM ID
# 22 F1 89 Version string
# 22 F1 8E Product code
# 22 F1 90 VIN - only 7e0
# 22 F1 97 System String

# Subaru Crosstrek 2018 ECU list
#
# TX    System String
# 0x735 Keyless Entry System
# 0x746 Power Steering System
# 0x747 Automatic Headlight Leveling
# 0x752 Integ. Unit mode
# 0x753 Tire pressure monitor
# 0x756 Occupant Detection System *
# 0x780 Airbag System
# 0x783 METER
# 0x787 EyeSight System
# 0x7b0 VDC/Parking Brake System
# 0x7c4 Air Condition System
# 0x7d0 Infotainment System
# 0x7e0 2.0 DOHC
# 0x7e1 CVT
# 0x7f1 Airbag System
#
# Note: 0x756 responds in accessory mode only
# See also: https://drive.google.com/drive/folders/0B7lZHaN-VSRGOVNUR0dlU09mZm8

if __name__ == "__main__":
  panda = Panda()
  panda.set_safety_mode(Panda.SAFETY_ELM327)
  # 0 - white/grey panda in OBD2, 1 - black panda/comma two + CPv2 in OBD2
  bus = 0
  panda.can_clear(bus)

  cmd = b'\x22\xf1\x97'  # ECU system string query
  #cmd = b'\x22\x10\x56' # Infotainment unit (7d0) volume check

  # set ecu tx addr
  tx_addr = 0x7d0
  rx_addr = tx_addr + 8

  print('0x%x ' % tx_addr + ''.join(r'\x{:02x}'.format(x) for x in cmd))

  while True:
    isotp_send(panda, cmd, tx_addr, bus)
    ret = isotp_recv(panda, rx_addr, bus)
    hexdump(ret)
    time.sleep(0.2)
    panda.send_heartbeat()
    break
