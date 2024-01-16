import subprocess
import struct
import datetime

def milliseconds_since_midnight():
    now = datetime.datetime.now()
    midnight = datetime.datetime(now.year, now.month, now.day)
    return int((now - midnight).total_seconds() * 1000)

def run_canusb_tool(command_args):
    # Assuming the compiled C code is named 'canusb_tool'
    result = subprocess.run(['/home/arkad94/USB-CAN-A/canusb'] + command_args, capture_output=True, text=True)
    return result.stdout.strip()

def main():
    # Ask the user for the number of times to run the loop (v)
    v = int(input("Enter the number of times to run the loop (v): "))

    for _ in range(v):
        # Example of receiving a CAN message
        received_data = run_canusb_tool(['-t', '-d', '/dev/ttyUSB0', '-s', '500000', '-t'])
        # Assuming the first 4 bytes are the time sent by Script 1
        sent_time = struct.unpack('I', bytes.fromhex(received_data[:8]))[0]

        # Check if received_data is empty (no message received)
        if not received_data:
            print("No CAN message received.")
            continue  # Skip the rest of the loop
        
        # Calculate latency (a1)
        current_time = milliseconds_since_midnight()
        a1 = current_time - sent_time

        print(f"a1: {a1} milliseconds")  # Print the value of a1 for debugging

        # Prepare the data to send back: a1 and current time
        response_data = struct.pack('II', a1, current_time).hex()

        # Send the response message
        run_canusb_tool(['-t', '-d', '/dev/ttyUSB0', '-s', '500000', '-i', '749', '-j', response_data, '-n', '1'])

if __name__ == '__main__':
    main()
