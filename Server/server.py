import socket
from decode_v4 import begin_decoding

def main():
    host = '0.0.0.0'  # Listen on all interfaces
    port = 8080
    buffer_size = 4000
    backlog = 1

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((host, port))
    print(f"Done with binding with IP: {host}, Port: {port}")
    
    server_socket.listen(backlog)
    print("Waiting for a connection...")
    
    client_socket, client_address = server_socket.accept()
    print(f"Client connected at IP: {client_address[0]} and port: {client_address[1]}")
    
    receivedtext = []
    try:
        while True:
            received_byte = client_socket.recv(1)
            
            #start decoding
            if not received_byte or received_byte == b'\n':
            	print("End message detected")
            	print(begin_decoding(receivedtext))
            	break
            else:
            	receivedtext.append(received_byte)
            	print("Message from client is: ", received_byte.decode('utf-8'))

    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        client_socket.close()
        print(f"Client at IP: {client_address[0]} and port: {client_address[1]} disconnected")
    
    server_socket.close()

if __name__ == "__main__":
    main()

