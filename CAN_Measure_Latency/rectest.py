import subprocess

def run_canusb_tool(command_args):
    try:
        result = subprocess.run(['/home/arkad94/USB-CAN-A/canusb'] + command_args, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Error output: {e.stderr}")
        return None

def main():
    while True:
        try:
            received_data = run_canusb_tool(['-t', '-d', '/dev/ttyUSB0', '-s', '500000'])

            if received_data is None:
                print("Error occurred while running the CAN tool.")
                break

            if not received_data:
                print("No CAN message received.")
                continue

            print(f"Received data: {received_data}")
        except Exception as ex:
            print(f"Exception: {ex}")

if __name__ == '__main__':
    main()
