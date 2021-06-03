#include <iostream>

#define HAVE_REMOTE
#include "pcap.h"

void print_addresses(u_char *user, const struct pcap_pkthdr* pkt_hdr, const u_char* data)
{
    /* 14 bytes for MAC header +
     * 12 byte offset into IP header for IP addresses
     */
    int offset = 26;
    std::cout << "Source address: " << +data[offset] << "." << +data[offset+1] << "." << +data[offset+2] << "." << +data[offset+3] << std::endl;
    std::cout << "Dest address  : " << +data[offset+4] << "." << +data[offset+5] << "." << +data[offset+6] << "." << +data[offset+7] << std::endl;
}

int main()
{
    pcap_t* pcap_file_desc;
    char errbuf[PCAP_ERRBUF_SIZE];

    // open capture file for offline processing
    pcap_file_desc = pcap_open_offline("1_packet.pcap", errbuf);
    if (pcap_file_desc == NULL) {
        std::cout << "pcap_open_offline() failed: " << errbuf << std::endl;
        return 1;
    }

    if (pcap_dispatch(pcap_file_desc, 0, &print_addresses, (u_char *)0) < 0) {
        return 1;
    }

    std::cout << "capture finished" << std::endl;

    pcap_close(pcap_file_desc);
    return 0;
}
