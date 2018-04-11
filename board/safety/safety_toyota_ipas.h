void can_send(CAN_FIFOMailBox_TypeDef *to_push, uint8_t bus_number);

// cap the speed at 10.25kph (1025). 1050 has been tested to be too high
const int speed_max = 1025;

// above 70 kph (45 mph), send the real speed
const int speed_cancel = 7000;

// entry state tracking
int angle_cmd_enable = 0;
int prev_angle_cmd_enable = 0;

// current state of the car
int current_speed = 0;
int ipas_rx_enable = 0;
int steer_override = 0;

static int toyota_ipas_fwd_hook(int bus_num, CAN_FIFOMailBox_TypeDef *to_fwd) {
  if (bus_num == 0) {

    // block 0x266 from IPAS
    if ((to_fwd->RIR>>21) == 0x266) {
      return -1;
    }

    if ((to_fwd->RIR>>21) == 0x167) {
      // change address
      to_fwd->RIR = (to_fwd->RIR & 0x1fffff) | (0x266 << 21);
      angle_cmd_enable = ((to_fwd->RDLR & 0xff) >> 4) == 3;
      if (!prev_angle_cmd_enable && angle_cmd_enable && current_speed < speed_cancel) {
        // send spoofed zero speed packet
        int speed = 0;
        int checksum = (0xb4 + 8 + speed + (speed >> 8)) & 0xff;

        CAN_FIFOMailBox_TypeDef to_send;
        to_send.RDLR = 0;
        to_send.RDHR = (checksum << 24) + ((speed & 0xff) << 16) + (speed & 0xff00);
        to_send.RDTR = 8;
        to_send.RIR = (0xb4 << 21) | 1;
        can_send(&to_send, 2);
      }
      prev_angle_cmd_enable = angle_cmd_enable;
      return 2;
    }
 
    if ((to_fwd->RIR>>21) == 0xb4) {
      int speed = ((to_fwd->RDHR) & 0xff00) | ((to_fwd->RDHR >> 16) & 0xff);
      current_speed = speed;

      if (speed > speed_max && speed < speed_cancel) {
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
      controls_allowed = ipas_rx_enable;
    }

    return 0;
  }
  return -1;
}

const safety_hooks toyota_ipas_hooks = {
  .init = nooutput_init,
  .rx = default_rx_hook,
  .tx = alloutput_tx_hook,
  .tx_lin = nooutput_tx_lin_hook,
  .fwd = toyota_ipas_fwd_hook,
};

