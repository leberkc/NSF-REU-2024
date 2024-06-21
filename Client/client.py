import socket
from fountain_client import generate_message

def main():
    server_ip = '10.9.0.6'  # IP address of the server
    port = 8080
    buffer_size = 1024

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, port))
        print("Connected to server")

        while True:
            client_message = input("Enter message to send to the server (or type 'exit' to disconnect): ")
            
            if client_message.lower() == 'exit':
                print("Disconnecting from server...")
                break
                
            encoded_bytes = generate_message(client_message)
            encoded_bytes += b'\n'
            for byte in encoded_bytes:
	            client_socket.sendall(byte)
            
            server_response = client_socket.recv(buffer_size)
            print("Server's response:", server_response.decode('utf-8'))

    except socket.error as e:
        print(f"Socket error: {e}")
    
    finally:
        client_socket.close()
        print("Disconnected from server")

if __name__ == "__main__":
    main()

