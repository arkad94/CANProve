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


def main():
    # Static value for baud rate
    baud_rate = 500000  # 500 kHz
    

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
        start_time = time.time()
        while time.time() - start_time < 4:
            send_can_message(bus, 0x001, [0x01, 0x01, 0x01, 0x01, 0x01])
        time.sleep(0.5)  # Adjust the sleep interval as needed
            
        send_can_message(bus, 0x007, [0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(0.5000)    
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
