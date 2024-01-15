import time
import can

# Function to send a CAN message and wait for acknowledgment
def send_and_receive(bus):
    try:
        message = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5, 6, 7], is_extended_id=False)
        bus.send(message)
        send_time = time.time()
        message = bus.recv(1.0)  # Timeout after 1 second
        if message is not None:
            recv_time = time.time()
            return (recv_time - send_time) * 1000  # Convert seconds to milliseconds
    except can.CanError as e:
        print("Error: ", e)
    return None

# Main execution
latencies = []
bus = can.interface.Bus(channel='can0', bustype='socketcan')

for _ in range(5):
    latency_ms = send_and_receive(bus)
    if latency_ms is not None:
        latencies.append(latency_ms)

bus.shutdown()

if latencies:
    average_latency_ms = sum(latencies) / len(latencies)
    print(f"Average round-trip latency: {average_latency_ms:.2f} ms")
else:
    print("No latencies were recorded.")
