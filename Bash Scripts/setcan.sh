#!/bin/bash

# Prompt for the baud rate
echo "Please enter the desired CAN baud rate:"
read baudrate

# Assuming the CAN interface is can0
CAN_INTERFACE="can0"

# Take the CAN network down
sudo ip link set down $CAN_INTERFACE

# Set the new baud rate
sudo ip link set $CAN_INTERFACE type can bitrate $baudrate

# Bring the CAN network back up
sudo ip link set up $CAN_INTERFACE

# Display the new settings
echo "The CAN network $CAN_INTERFACE is now set to $baudrate bps"
