import can
import time

def send_can_message(bus, message_id, data):
    byte_data = bytes(data)
    msg = can.Message(arbitration_id=message_id, data=byte_data, is_extended_id=False)
    try:
        bus.send(msg)
        print(f"Message {byte_data.hex()} sent on {message_id:#x}")
    except can.CanError:
        print("Message NOT sent")


def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(i)
        time.sleep(1)        

def main():
    # User input for baud rate
    baud_rate_input = input("Select baud rate: 1 for 500 kHz, 2 for 1 MHz: ")
    baud_rate = 500000 if baud_rate_input == '1' else 1000000

    # Countdown
    print("Starting countdown...")
    countdown(10)
    print("Countdown complete. Starting CAN communication.")

    # Configure CAN interface
    bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=baud_rate)

    try:
        # Original sequence of CAN messages
        send_can_message(bus, 0x007, [0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(0.0005)
        send_can_message(bus, 0x007, [0x01, 0x00, 0x00, 0x00, 0x00])
        time.sleep(5)
        send_can_message(bus, 0x007, [0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(0.0005)
        send_can_message(bus, 0x002, [0x01, 0x01, 0x00, 0x00, 0x00, 0x00])
        time.sleep(4)
        send_can_message(bus, 0x002, [0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(0.0005)
        send_can_message(bus, 0x007, [0x00, 0x00, 0x00, 0x00, 0x01])
        time.sleep(5)
        send_can_message(bus, 0x007, [0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(0.0005)    
        send_can_message(bus, 0x002, [0x00, 0x00, 0x00, 0x00, 0x01, 0x01])
        time.sleep(5)
        send_can_message(bus, 0x007, [0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(0.0005)



    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, shutting down.")
    finally:
        # Cleanly close the CAN bus interface
        bus.shutdown()
        print("CAN interface closed.")

    print("Sequence complete")

if __name__ == "__main__":
    main()
