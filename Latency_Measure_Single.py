import time
import can

def send_and_receive():
    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan')
        # Send a CAN message with ID 0x10 and some data
        message = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5, 6, 7], is_extended_id=False)
        bus.send(message)
        send_time = time.time()
        print(f"Message sent at {send_time}")

        # Wait for any incoming CAN message
        while True:
            message = bus.recv(1.0)  # Timeout after 1 second
            if message is not None:
                recv_time = time.time()
                print(f"Message received at {recv_time}")
                return send_time, recv_time
            else:
                print("Timeout occurred, no message received.")
                break  # Exit the loop if no message is received within the timeout period

    except can.CanError as e:
        print("Error: ", e)
    finally:
        if bus:
            bus.shutdown()        

# Initialize variables for send and receive times
send_time = None
recv_time = None

try:
    send_time, recv_time = send_and_receive()
except TypeError:
    print("Did not receive any CAN messages in time.")



# Calculate and print the latency only if both send and receive times are available
if send_time and recv_time:
    latency = recv_time - send_time
    print(f"Round-trip latency: {latency} seconds")
else:
    print("Unable to calculate latency without both send and receive times.")

 


