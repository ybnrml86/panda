
static int toyota_ipas_fwd_hook(int bus_num, CAN_FIFOMailBox_TypeDef *to_fwd) {
  if (bus_num == 0) {
    if ((to_fwd->RIR>>21) == 0xb4) {
      // cap the speed at 10.25kph (1025). 1050 has been tested to be too high
      const int speed_max = 1025;
      int speed = ((to_fwd->RDHR) & 0xff00) | ((to_fwd->RDHR >> 16) & 0xff);
      if (speed > speed_max) {
        speed = speed_max;
      }
      int checksum = (0xb4 + 8 + speed + (speed >> 8)) & 0xff;
      to_fwd->RDLR = 0;
      to_fwd->RDHR = (checksum << 24) + ((speed & 0xff) << 16) + (speed & 0xff00);
    }

    return 2;
  }
  if (bus_num == 2) {
    return 0;
  }
  return -1;
}

const safety_hooks toyota_ipas_hooks = {
  .init = alloutput_init,
  .rx = default_rx_hook,
  .tx = alloutput_tx_hook,
  .tx_lin = nooutput_tx_lin_hook,
  .fwd = toyota_ipas_fwd_hook,
};

