import can
import time
import struct
eimport pandas as pd
import os
from datetime import datetime

def milliseconds_since_midnight():
    now = datetime.now()
    midnight = datetime(now.year, now.month, now.day)
    return int((now - midnight).total_seconds() * 1000)  # Convert to milliseconds
  # Convert to milliseconds

def send_can_message(bus, arbitration_id):
    current_time = milliseconds_since_midnight()
    data = struct.pack('I', current_time)  # Pack the time into 4 bytes
    message = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        return current_time
    except can.CanError:
        print("Message NOT sent")
        return None

def receive_response(bus, arbitration_id):
    while True:
        message = bus.recv(10.0)  # Timeout in seconds
        if message is None:
            print("Timeout occurred, no message.")
            return None, None
        if message.arbitration_id == arbitration_id:
            recv_time = milliseconds_since_midnight()
            return message, recv_time

def calculate_latency(sent_time, recv_time):
    if recv_time is None:
        return None
    latency = recv_time - sent_time
    return latency / 1000.0  # Convert to seconds

def main():
    global bus
    bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)
    v = int(input("Enter the number of iterations (v): "))
    mode = input("Enter Mode (Y/N): ").strip().lower()  # Accept 'y' or 'n'
    total_latency = 0
    valid_responses = 0

    records = []

    for _ in range(v):
        sent_time = send_can_message(bus, 749)
        if sent_time is None:
            continue

        response, recv_time = receive_response(bus, 749)
        latency = calculate_latency(sent_time, recv_time)

        if latency is not None:
            total_latency += latency
            valid_responses += 1
            records.append([sent_time, recv_time, latency])
        else:
            records.append([sent_time, "No response", "N/A"])

        if response is None and mode == 'n':
            break

    # This part should be indented to be inside the main() function
    df = pd.DataFrame(records, columns=['Sent Time', 'Received Time', 'Latency (s)'])

    if valid_responses > 0:
        average_latency = total_latency / valid_responses
        print(f"Average latency: {average_latency} seconds")
        
        # Append average latency using pandas.concat
        avg_df = pd.DataFrame([{'Latency (s)': 'Average Latency', 'Sent Time': '', 'Received Time': average_latency}])
        df = pd.concat([df, avg_df], ignore_index=True)
    else:
        print("No valid responses received.")

    # Create output folder if it doesn't exist
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # Include current timestamp in the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_filename = os.path.join(output_folder, f"CAN_test_results_{timestamp}.xlsx")

    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='LatencyData')

    print(f"Results saved to {excel_filename}")

    # Save the DataFrame to an Excel file
    excel_filename = os.path.join(output_folder, "CAN_test_results.xlsx")
    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='LatencyData')

    print(f"Results saved to {excel_filename}")

if __name__ == "__main__":
    bus = None
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        print("Closing CAN bus.")
        if bus:
            bus.shutdown()
