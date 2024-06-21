#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <errno.h>
#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <openssl/hmac.h>
#include <netinet/in.h>
#include <unistd.h>
#define PORT 8080

void handleErrors(void);

void handleErrors(){
    ERR_print_errors_fp(stderr);
    abort();
}

int main(int argc, char const* argv[])
{
    int server_fd, new_socket, valread;
    struct sockaddr_in address;
    int opt = 1;
    socklen_t addrlen = sizeof(address);
	
    char* hello = "Hello from server";
    unsigned char receivedtext[4000] = {0};
	
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }
 
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);
 
    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
    printf("Done with binding with IP: %s, Port: %d\n", "10.9.0.5", 8080);
    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }
    if ((new_socket = accept(server_fd, (struct sockaddr*)&address, &addrlen)) < 0) {
        perror("accept");
        exit(EXIT_FAILURE);
    }
	printf("Client connected at IP: %s and port: %i\n", "10.9.0.1", 8080);
	
    valread = read(new_socket, receivedtext, 3000-1);
  

    printf("Message from client is:\n");
    printf("%s\n", receivedtext);

    if(send(new_socket, hello, strlen(hello), 0) < 0) {
    	perror("Could not send hello.");
    	close(new_socket);
    	close(server_fd);
    	exit(EXIT_FAILURE);
    }
    printf("Hello message sent\n");
 
    close(new_socket);

    close(server_fd);
    return 0;
}

