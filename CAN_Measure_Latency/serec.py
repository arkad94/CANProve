import can
import time
import struct
import datetime

def milliseconds_since_midnight():
    now = datetime.datetime.now()
    midnight = datetime.datetime(now.year, now.month, now.day)
    return int((now - midnight).total_seconds() * 1000)  # Convert to milliseconds

def send_can_message(bus, arbitration_id):
    current_time = milliseconds_since_midnight()
    data = struct.pack('I', current_time)  # Pack the time into 4 bytes
    message = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print(f"Message sent on {bus.channel_info}")
    except can.CanError:
        print("Message NOT sent")

def receive_response(bus, arbitration_id):
    while True:
        message = bus.recv(10.0)  # Timeout in seconds
        if message is None:
            print("Timeout occurred, no message.")
            return None
        if message.arbitration_id == arbitration_id:
            return message

def calculate_latency(sent_time, response_message):
    if response_message is None:
        return None
    received_time = time.time()
    latency = received_time - sent_time
    return latency

def main():
    global bus
    bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)
    v = int(input("Enter the number of iterations (v): "))
    mode = input("Enter Mode (Y/N): ").strip().lower()  # Accept 'y' or 'n'
    total_latency = 0
    valid_responses = 0

    for _ in range(v):
        sent_time = time.time()
        send_can_message(bus, 749)  # Modified call without the additional data array
        response = receive_response(bus, 749)

        if response is None:
            print("No response received for message with arbitration ID 749.")
            if mode == 'y':
                continue  # If 'Y' is selected, skip to the next iteration immediately
            else:
                break  # If 'N' is selected, end the loop after a timeout

        latency = calculate_latency(sent_time, response)
        if latency is not None:
            total_latency += latency
            valid_responses += 1
            print(f"Latency for iteration: {latency} seconds")

    if valid_responses > 0:
        average_latency = total_latency / valid_responses
        print(f"Average latency: {average_latency} seconds")
    else:
        print("No valid responses received.")



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        print("Closing CAN bus.")
        if bus:
            bus.shutdown() 
