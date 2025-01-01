#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

// Function to calculate CRC-CCITT (16-bit)
uint16_t crc_ccitt_16_bitstream(const char *bitstream, uint16_t poly, uint16_t init_crc) {
    uint16_t crc = init_crc;
    for (size_t i = 0; i < strlen(bitstream); i++) {
        crc ^= ((bitstream[i] - '0') << 15); // Align the bit with CRC's uppermost bit
        for (int j = 0; j < 1; j++) {       // Process the single bit
            if (crc & 0x8000) {             // Check if the leftmost bit is set
                crc = (crc << 1) ^ poly;
            } else {
                crc <<= 1;
            }
            crc &= 0xFFFF;                  // Ensure CRC remains 16-bit
        }
    }
    return crc;
}

// Function to append CRC to the bitstream
void append_crc_to_bitstream(const char *bitstream, char *output) {
    uint16_t crc = crc_ccitt_16_bitstream(bitstream, 0x1021, 0xFFFF);
    sprintf(output, "%s%016b", bitstream, crc); 
}

// Function to verify CRC in the received bitstream
bool verify_crc_bitstream(const char *bitstream_with_crc) {
    size_t len = strlen(bitstream_with_crc);
    if (len < 16) {
        return false; // Not enough bits to contain CRC
    }

    char data[len - 16 + 1];
    strncpy(data, bitstream_with_crc, len - 16);
    data[len - 16] = '\0'; // Null-terminate the string

    char received_crc_str[17];
    strncpy(received_crc_str, bitstream_with_crc + len - 16, 16);
    received_crc_str[16] = '\0'; // Null-terminate the CRC string

    uint16_t received_crc = (uint16_t)strtol(received_crc_str, NULL, 2);
    uint16_t calculated_crc = crc_ccitt_16_bitstream(data, 0x1021, 0xFFFF);

    return calculated_crc == received_crc;
}

int main() {
    char message_bits[256];
    char bitstream_with_crc[512];
    char user_bitstream[512];

    // User input for the original bitstream
    printf("Enter the original bitstream (e.g., 11010011101100): ");
    scanf("%s", message_bits);

    // Calculate and append CRC
    append_crc_to_bitstream(message_bits, bitstream_with_crc);
    printf("Bitstream with CRC: %s\n", bitstream_with_crc);

    // User input for verification
    printf("Enter the received bitstream for verification (e.g., 11010011101100110110110111000011): ");
    scanf("%s", user_bitstream);

    // Verify CRC
    bool is_valid = verify_crc_bitstream(user_bitstream);
    printf("CRC valid: %s\n", is_valid ? "true" : "false");

    return 0;
}
