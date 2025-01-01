#include <stdio.h>
#include <string.h>

char data[20], check_value[30], poly[10];
int data_length, poly_length;

void XOR() {
    for (int j = 1; j < poly_length; j++) {
        check_value[j] = (check_value[j] == poly[j]) ? '0' : '1';
    }
}

void crc() {
    for (int i = 0; i < poly_length; i++) {
        check_value[i] = data[i];
    }

    int current_bit = poly_length;
    do {
        if (check_value[0] == '1') XOR();
        for (int j = 0; j < poly_length - 1; j++) {
            check_value[j] = check_value[j + 1];
        }
        check_value[poly_length - 1] = data[current_bit++];
    } while (current_bit <= data_length + poly_length - 1);
}

void receiver() {
    printf("Enter the received data: ");
    scanf("%s", data);

    printf("Data received: %s\n", data);

    crc();

    int error_found = 0;
    for (int i = 0; i < poly_length - 1; i++) {
        if (check_value[i] == '1') {
            error_found = 1;
            break;
        }
    }

    if (error_found) {
        printf("Error detected\n");
    } else {
        printf("No error detected\n");
    }
}

int main() {
    printf("Enter data to be transmitted: ");
    scanf("%s", data);

    printf("Enter the divisor polynomial: ");
    scanf("%s", poly);

    data_length = strlen(data);
    poly_length = strlen(poly);

    // Pad data with zeros
    for (int i = data_length; i < data_length + poly_length - 1; i++) {
        data[i] = '0';
    }
    data[data_length + poly_length - 1] = '\0';

    printf("Data padded with n-1 zeroes: %s\n", data);

    crc();

    printf("CRC value is: %s\n", check_value);

    // Append CRC to data
    for (int i = data_length; i < data_length + poly_length - 1; i++) {
        data[i] = check_value[i - data_length];
    }
    data[data_length + poly_length - 1] = '\0';

    printf("Final codeword to be sent: %s\n", data);

    receiver();

    return 0;
}
