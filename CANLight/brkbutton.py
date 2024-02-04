import can
import time
import threading
import select
import sys

def send_messages(bus, message, stop_event, continue_event):
    while not stop_event.is_set():
        if continue_event.is_set():
            bus.send(message)
            print("Brake actuated!")
            time.sleep(0.003)  # Sleep for 3 milliseconds
        else:
            time.sleep(0.1)  # Sleep when paused

def user_input_handler(continue_event, stop_event):
    print("Type '.' to pause/resume sending messages. Type 'quit' to exit.")
    while not stop_event.is_set():
        user_input = input()
        if user_input == '.':
            if continue_event.is_set():
                continue_event.clear()  # Stop sending messages
                print("Sending paused.")
            else:
                continue_event.set()  # Resume sending messages
                print("Sending resumed.")
        elif user_input == 'quit':
            stop_event.set()

def main():
    # Ask the user to select the baud rate
    while True:
        baud_rate_input = input("Select the baud rate (1 for 500 KHz, 2 for 1 MHz): ")
        if baud_rate_input in ['1', '2']:
            break
        else:
            print("Invalid input. Please enter 1 or 2.")

    if baud_rate_input == '1':
        bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)
    else:
        bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=1000000)

    message = can.Message(arbitration_id=0x001, data=[0x01, 0x01, 0x01, 0x01, 0x01])

    stop_event = threading.Event()
    continue_event = threading.Event()
    continue_event.set()  # Initially allow message sending

    can_thread = threading.Thread(target=send_messages, args=(bus, message, stop_event, continue_event))
    input_thread = threading.Thread(target=user_input_handler, args=(continue_event, stop_event))

    can_thread.start()
    input_thread.start()

    # Wait for threads to finish
    can_thread.join()
    input_thread.join()
    bus.shutdown()
    sys.exit(0)

if __name__ == "__main__":
    main()
