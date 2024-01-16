import can

def send_can_message(bus, arbitration_id, data_payload):
    # Create a CAN message
    message = can.Message(arbitration_id=arbitration_id, data=data_payload, is_extended_id=False)
    try:
        bus.send(message)
        print(f"Message sent on {bus.channel_info}: {message}")
    except can.CanError:
        print("Message NOT sent")

# Example usage
if __name__ == "__main__":
    # Set up your CAN bus interface (adjust as per your setup)
    bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)

    # Arbitration ID
    arbitration_id = 0x2ED  # 749 in decimal

    # Data payload in bytes
    data_payload = bytes.fromhex('BEED')

    # Send the CAN message
    send_can_message(bus, arbitration_id, data_payload)
