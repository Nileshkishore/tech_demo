import threading
import time
import subprocess
import os

# Define the function that runs the script
def run_ingest():
    while True:
        try:
            # Run the ingest.py script
            subprocess.run(['python', 'ingest_test.py'], check=True)
        except subprocess.CalledProcessError as e:
            # Handle errors in script execution
            print(f"Error running ingest.py: {e}")
        time.sleep(60)  # Wait for 60 seconds before running again

# Define the function to start the background task
def start_background_task():
    # Create and start a daemon thread for the background task
    thread = threading.Thread(target=run_ingest)
    thread.daemon = True  # Ensure the thread exits when the main program exits
    thread.start()
