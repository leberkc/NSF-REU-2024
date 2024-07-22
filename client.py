
import socket, random
from encoder import start

if __name__ == "__main__":
    #server_ip = '10.9.0.6'  # IP address of the server
    server_ip = '192.168.4.19'
    #server_ip = '198.145.146.237'

    port = 8080
    buffer_size = 1024
    num_trials = 2

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((server_ip, port))
        total_packets_received = 0
        total_packets_processed = 0
        num_trials = 1000

        print("Connected to server")
        
        client_message = input("Enter message to send to the server (or type 'exit' to disconnect): ")
            
        if client_message.lower() == 'exit':
            print("Disconnecting from server...")
            exit()

        for _ in range(num_trials):
            start(client_socket, client_message)

    except socket.error as e:
        print(f"Socket error: {e}")

    finally:
        client_socket.close()
        #print("Disconnected from server")

    # avg_packets_received = total_packets_received / num_trials
    # avg_packets_processed = total_packets_processed / num_trials
    # print(f"Average Packets Received: {avg_packets_received}")
    # print(f"Average Packets Processed: {avg_packets_processed}")