#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/time.h> // for gettimeofday
#include <linux/can.h>
#include <linux/can/raw.h>

int main() {
    int s; // Socket file descriptor
    struct sockaddr_can addr;
    struct ifreq ifr;
    struct can_frame frame;
    struct timeval tv;
    unsigned long long milliseconds_since_midnight;
    int v; // Number of iterations for the loop
    unsigned long long total_latency = 0; // To calculate the average latency

    // Ask the user for the number of iterations 'v'
    printf("Enter the number of iterations: ");
    scanf("%d", &v);

    // Create a socket
    if ((s = socket(PF_CAN, SOCK_RAW, CAN_RAW)) < 0) {
        perror("Error while opening socket");
        return -1;
    }

    // Specify can0 interface
    strcpy(ifr.ifr_name, "can0");
    ioctl(s, SIOCGIFINDEX, &ifr);

    // Bind the socket to can0
    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;
    if (bind(s, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("Error in socket bind");
        return -2;
    }

    for (int i = 0; i < v; i++) {
        // Get current time
        gettimeofday(&tv, NULL);
        milliseconds_since_midnight = (tv.tv_sec % 86400) * 1000 + tv.tv_usec / 1000;

        // Prepare a CAN frame with current time as data
        frame.can_id = 0x749;
        frame.can_dlc = 8;
        memcpy(frame.data, &milliseconds_since_midnight, sizeof(milliseconds_since_midnight));

        // Send the CAN frame
        if (write(s, &frame, sizeof(struct can_frame)) != sizeof(struct can_frame)) {
            perror("Error writing to CAN");
            return -3;
        }

        // Wait for response
        if (read(s, &frame, sizeof(struct can_frame)) < 0) {
            perror("Error reading from CAN");
            return -4;
        }

        // Process received frame: extract a1 and calculate total latency
        unsigned long long received_time, a1;
        memcpy(&a1, frame.data, sizeof(a1));
        gettimeofday(&tv, NULL);
        received_time = (tv.tv_sec % 86400) * 1000 + tv.tv_usec / 1000;

        unsigned long long a2 = received_time - milliseconds_since_midnight;
        total_latency += a1 + a2;
    }

    // Calculate and print the average latency
    printf("Average latency over %d iterations: %llu milliseconds\n", v, total_latency / v);

    // Close the socket
    close(s);

    return 0;
}

