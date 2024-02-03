import can
import time
import sys
import threading
import select

def send_messages(bus, message, stop_event):
    while not stop_event.is_set():
        bus.send(message)
        print("Brake actuated!")
        time.sleep(0.003)  # Sleep for 3 milliseconds

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
    thread = threading.Thread(target=send_messages, args=(bus, message, stop_event))
    thread.start()

    print("Type '.' to stop sending messages.")
    try:
        while True:
            # Non-blocking input using select
            if select.select([sys.stdin], [], [], 0)[0]:
                user_input = sys.stdin.readline().strip()
                if user_input == '.':
                    stop_event.set()
                    break
    except KeyboardInterrupt:
        print("Script terminated by keyboard interrupt.")
        stop_event.set()
    finally:
        thread.join()
        bus.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()
