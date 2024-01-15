import can
import time

def send_timestamped_message(channel='can0', bitrate=1000000):
    # Initialize the CAN bus interface
    bus = can.interface.Bus(channel=channel, bustype='socketcan', bitrate=bitrate)

    # Get the current time in milliseconds
    timestamp = int(time.time() * 1000)
    # Convert the timestamp to bytes (ensure it fits in 8 bytes)
    data = timestamp.to_bytes(8, byteorder='big')

    # Create a CAN message with an arbitrary arbitration ID (e.g., 0x123)
    message = can.Message(arbitration_id=0x123, data=data, is_extended_id=False)

    # Send the message
    try:
        bus.send(message)
        print(f"Message sent with timestamp: {timestamp}")
    except can.CanError as e:
        print("Message NOT sent: ", e)

    # Cleanup
    bus.shutdown()

if __name__ == "__main__":
    send_timestamped_message()
