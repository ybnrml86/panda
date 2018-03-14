// cap the speed at 10.25kph (1025). 1050 has been tested to be too high
const int speed_max = 1025;
const int counter_max = 50;

int ipas_rx_enable = 0;
int angle_cmd_enable = 0;
int zero_speed_cnt = counter_max;   // 2s, since 0xb4 msg is updated at 40Hz
int steer_override = 0;

static int toyota_ipas_fwd_hook(int bus_num, CAN_FIFOMailBox_TypeDef *to_fwd) {
  if (bus_num == 0) {
    if ((to_fwd->RIR>>21) == 0x266) {
      angle_cmd_enable = ((to_fwd->RDLR & 0xff) >> 4) == 3;
    }
 
    if ((to_fwd->RIR>>21) == 0xb4) {

      int speed = ((to_fwd->RDHR) & 0xff00) | ((to_fwd->RDHR >> 16) & 0xff);

      if (angle_cmd_enable && (!ipas_rx_enable) && (!steer_override)) {
        zero_speed_cnt = 0;
      } else if (ipas_rx_enable) {
        zero_speed_cnt = counter_max;
      }

      if (zero_speed_cnt < counter_max) {
        speed = 0;
        zero_speed_cnt += 1;
      } else if (speed > speed_max) {
        speed = speed_max;
      }

      // reconstruct speed packet
      int checksum = (0xb4 + 8 + speed + (speed >> 8)) & 0xff;
      to_fwd->RDLR = 0;
      to_fwd->RDHR = (checksum << 24) + ((speed & 0xff) << 16) + (speed & 0xff00);
    }

    return 2;
  }

  if (bus_num == 2) {
    if ((to_fwd->RIR>>21) == 0x260) {
      const int torque_override_thrs = 100;
      int16_t torque_driver = (((to_fwd->RDLR) & 0xFF00) | ((to_fwd->RDLR >> 16) & 0xFF));
      steer_override = (torque_driver > torque_override_thrs) || (torque_driver < -torque_override_thrs);
    }

    if ((to_fwd->RIR>>21) == 0x262) {
      ipas_rx_enable = (to_fwd->RDLR & 0xf) == 3;
    }

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

