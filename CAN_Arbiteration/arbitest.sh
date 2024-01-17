#!/bin/bash

# Start the first command in the background
/home/arkad94/USB-CAN-A/./canusb -d /dev/ttyUSB0 -s 500000 -tn -2 -i 1 -j BAA -n 20 &

# Start the second command in the background
/home/arkad94/USB-CAN-A/./canusb -d /dev/ttyUSB0 -s 500000 -tn -1 -i 2 -j BAA -n 20 &

# Wait for both background processes to finish
wait
