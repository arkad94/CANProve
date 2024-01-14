import time
import can
import pandas as pd

def send_and_receive(bus):
    try:
        # Send a CAN message with ID 0x123 and some data
        message = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5, 6, 7], is_extended_id=False)
        bus.send(message)
        send_time = time.time()
        # Wait for any incoming CAN message
        message = bus.recv(1.0)  # Timeout after 1 second
        if message is not None:
            recv_time = time.time()
            return recv_time - send_time
    except can.CanError as e:
        print("Error: ", e)
    return None

# Initialize variables
latencies = []

# Initialize CAN bus
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Perform the send and receive 80 times
for _ in range(80):
    latency = send_and_receive(bus)
    if latency is not None:
        latencies.append(latency)

# Shutdown the CAN bus after the operations
bus.shutdown()

# Calculate and print the average latency
if latencies:
    average_latency = sum(latencies) / len(latencies)
    print(f"Average round-trip latency: {average_latency} seconds")
    
    # Create a DataFrame from the latencies
    df = pd.DataFrame(latencies, columns=['Latency'])
    print(df)
else:
    print("No latencies were recorded.")

# Save the DataFrame to a CSV file
df.to_csv('latency_measurements.csv', index=False)
