
import socket
from decoder import start    

if __name__ == "__main__":
    host = '0.0.0.0'  # Listen on all interfaces
    port = 8080
    backlog = 1

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((host, port))
    print(f"Done with binding with IP: {host}, Port: {port}")
    
    server_socket.listen(backlog)
    print("Waiting for a connection...")

    try:
        total_packets_received = 0
        total_packets_processed = 0
        total_code_rate = 0
        num_trials = 1000
        list_packets_received = []
        list_code_rate = []

        client_socket, client_address = server_socket.accept()
        print(f"Client connected at IP: {client_address[0]} and port: {client_address[1]}")
        
        try:
            for _ in range(num_trials):
                packets_received, packets_processed, code_rate = start(client_socket)
                #list_packets_received.append(packets_received)
                list_code_rate.append(code_rate)
                total_packets_received += packets_received
                total_packets_processed += packets_processed
                total_code_rate += code_rate

            avg_packets_received = total_packets_received / num_trials
            avg_packets_processed = total_packets_processed / num_trials
            avg_code_rate = total_code_rate / num_trials

            print("\nGlobal Stats:")
            for i in range(len(list_code_rate)):
                print(list_code_rate[i])
            print()
            print(f"\tNumber of Trials: {num_trials}")
            print(f"\tAverage Packets Received: {avg_packets_received}")
            print(f"\tAverage Packets Processed: {avg_packets_processed}")
            print(f"\tAverage Code Rate: {avg_code_rate}\n")

        except socket.error as e:
            print(f"Socket error: {e}")
        finally:
            client_socket.close()
            print(f"Client at IP: {client_address[0]} and port: {client_address[1]} disconnected")
    finally:
        server_socket.close()
