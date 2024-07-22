import subprocess
import time
import os

DEBUG = False

def run_server():
    return subprocess.Popen(['python3', 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def run_client():
    return subprocess.Popen(['python3', 'client.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def read_output(process):
    while True:
        output = process.stdout.readline()
        if output:
            print(output.strip())
        else:
            break
    while True:
        error = process.stderr.readline()
        if error:
            print(error.strip())
        else:
            break

if __name__ == "__main__":
    for _ in range(1000):
        try:
            # Start the server
            if DEBUG: print("Starting server...")
            server_process = run_server()
            time.sleep(1)  # Give the server some time to start

            # Start the client
            if DEBUG: print("Starting client...")
            client_process = run_client()

            # Send "Hello World" to the client
            if DEBUG: print("Sending input to client...")
            client_process.stdin.write("Meow\n")
            client_process.stdin.flush()

            # Read client output
            read_output(client_process)

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Terminate the server process
            if server_process:
                server_process.terminate()
                read_output(server_process)
    print("runner done!")