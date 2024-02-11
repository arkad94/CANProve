import requests
import time
import subprocess
import logging
import os

# Setup basic logging
logging.basicConfig(level=logging.INFO)

HEROKU_APP_URL = "https://jlo-ai-6b18b35d51db.herokuapp.com"

def get_cpu_temperature():
    temp = os.popen("vcgencmd measure_temp").readline()
    return temp.replace("temp=", "").replace("'C\n", "") + "°C"

def main():
    last_temp_time = time.time()

    while True:
        current_time = time.time()

        # Check and print temperature every 10 seconds
        if current_time - last_temp_time >= 10:
            cpu_temp = get_cpu_temperature()
            print(f"CPU Temperature: {cpu_temp}")
            last_temp_time = current_time

        try:
            logging.info("Polling for commands...")
            response = requests.get(f"{HEROKU_APP_URL}/canlight/get-command")
            if response.status_code == 200:
                command = response.json().get('command')
                if command:
                    logging.info(f"Received command: {command}")
                    if command == "execute_ctrl":
                        logging.info("Executing poc script")
                        subprocess.run(['python3', '/home/arkad94/CANProve/CANLight/pocrelay.py'])
                else:
                    logging.info("No command received.")
            else:
                logging.error(f"Error in response: {response.status_code}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        time.sleep(0.1)  # Poll every 0.5 seconds

if __name__ == "__main__":
    main()
