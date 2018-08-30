#!/bin/bash

enable_gpio () {
  cd /sys/class/gpio
  echo "$1" > export
  cd gpio$1
  echo "out" > direction
  echo "1" > value
  cd ../
}


# ST_RESET
enable_gpio 243
echo "0" > /sys/class/gpio/gpio243/value
sleep 0.1
echo "1" > /sys/class/gpio/gpio243/value

