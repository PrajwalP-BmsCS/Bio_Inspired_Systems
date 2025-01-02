#include <stdio.h>

int main() {
    int incoming, outgoing, bucket_size, n, store = 0;

    printf("Enter bucket size: ");
    scanf("%d", &bucket_size);

    printf("Enter outgoing rate: ");
    scanf("%d", &outgoing);

    printf("Enter the number of packets: ");
    scanf("%d", &n);

    while (n--) {
        printf("Enter the incoming packet size: ");
        scanf("%d", &incoming);

        if (incoming + store > bucket_size) {
            printf("Dropped %d number of packets\n", (incoming + store - bucket_size));
            store = bucket_size;
        } else {
            store += incoming;
        }

        printf("Bucket buffer size %d out of %d\n", store, bucket_size);

        store -= outgoing;

        if (store < 0) {
            store = 0;
        }

        printf("After outgoing %d packets left out of %d in buffer\n", store, bucket_size);
    }

    return 0;
}
