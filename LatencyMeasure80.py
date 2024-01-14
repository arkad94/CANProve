import time
import can
import pandas as pd
import os
from datetime import datetime

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

for _ in range(2):
    latency_ms = send_and_receive(bus)
    if latency_ms is not None:
        latencies.append(latency_ms)

bus.shutdown()

output_dir = 'outputs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if latencies:
    average_latency_ms = sum(latencies) / len(latencies)
    print(f"Average round-trip latency: {average_latency_ms:.2f} ms")

    # Adding the average latency to the DataFrame
    latencies_with_avg = [average_latency_ms] + latencies
    baud_rates = [0.5] * len(latencies_with_avg)
    df = pd.DataFrame({'Latency (ms)': latencies_with_avg, 'Baud Rate (MHz)': baud_rates})

    # Generate a unique filename
    timestamp_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    excel_filename = os.path.join(output_dir, f'latency_measurements_{timestamp_str}.xlsx')

    # Create a Pandas Excel writer using XlsxWriter as the engine
    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='LatencyData')

        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['LatencyData']

        # Add a format for bold text
        bold = workbook.add_format({'bold': True})

        # Write the column headers with bold formatting
        worksheet.write('A1', 'Latency (ms)', bold)
        worksheet.write('B1', 'Baud Rate (MHz)', bold)

else:
    print("No latencies were recorded.")