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

void handleErrors() {
    ERR_print_errors_fp(stderr);
    abort();
}

int main() {
	int status, valread, client_fd, ciphertext_len;
	struct sockaddr_in serv_addr;
	unsigned char client_message[1024];

	unsigned char *aad = "Authenticate";
    	int aad_len = strlen(aad);
	
	char buffer[1024] = { 0 };
	memset(buffer, 0, 1024);
		           
	if ((client_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
		printf("\n Socket creation error \n");
		return -1;
	}

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(PORT);

	if (inet_pton(AF_INET, "10.9.0.6", &serv_addr.sin_addr) <= 0) {
		printf("\nInvalid address/ Address not supported \n");
		return -1;
	}
	if ((status = connect(client_fd, (struct sockaddr*)&serv_addr, sizeof(serv_addr))) < 0) {
		printf("\nConnection Failed \n");
		return -1;
	}
	
	//printf("Enter message sent to the server: ");
	//fgets(client_message, 1024-1, stdin);
	system("python3 fountain_client.py");
	
	unsigned char tosend[6000];

	if(send(client_fd, client_message, sizeof(client_message), 0) < 0) {
		perror("Could not send the message.");
		exit(EXIT_FAILURE);
	}
	
	valread = read(client_fd, buffer, 1024 - 1); // subtract 1 for the null
						// terminator at the end
	printf("Server's response: %s\n", buffer);
	close(client_fd);
	return 0;
}
