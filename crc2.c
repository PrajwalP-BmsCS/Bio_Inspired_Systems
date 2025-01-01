#include <stdio.h>
#include <string.h>
#define N strlen(poly) // N is the length of the generator polynomial

char data[30];
char checksum[30];
char poly[10];
int datalen, i, j;

void XOR() {
    for (j = 0; j < N; j++) { // XOR operation starts from the first bit
        checksum[j] = (checksum[j] == poly[j]) ? '0' : '1';
    }
}

void crc() {
    // Copy the first N bits of data to checksum
    for (i = 0; i < N; i++) {
        checksum[i] = data[i];
    }

    do {
        if (checksum[0] == '1') {
            XOR(); // Perform XOR if the first bit is 1
        }

        // Shift left by one position
        for (j = 0; j < N - 1; j++) {
            checksum[j] = checksum[j + 1];
        }

        // Append the next bit from data
        checksum[j] = data[i++];

    } while (i < datalen + N - 1); // Continue until all bits are processed
}

void receiver() {
    printf("\nEnter the received data: ");
    scanf("%s", data);

    printf("Received Data: %s\n", data);

    datalen = strlen(data);
    crc();
    // Check if the checksum contains any non-zero bits
    for (i = 0; (i < N - 1) && (checksum[i] == '1'); i++);
    
    if (i < N - 1)
        printf("\nError detected in received data. %s\n",&checksum[i]);
    else
        printf("\nNo error detected in received data. %s\n",&checksum[i]);
}

int main() {
    printf("Enter the data bits: ");
    scanf("%s", data);

    printf("Enter the generator polynomial: ");
    scanf("%s", poly);

    datalen = strlen(data);

    // Append (N-1) zero bits to the data
    for (i = datalen; i < datalen + N - 1; i++) {
        data[i] = '0';
    }
    data[datalen + N - 1] = '\0'; // Null-terminate the string

    crc();

    printf("CRC Code: %s\n", checksum);

    receiver();

    return 0;
}


