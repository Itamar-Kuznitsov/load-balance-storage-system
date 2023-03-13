# import:
import random
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sendp, sniff


def send_discover(src_mac):
    pkt = Ether(dst='ff:ff:ff:ff:ff:ff', src=src_mac, type=0x0800) / IP(src='0.0.0.0', dst='255.255.255.255') / \
          UDP(dport=67, sport=68) / BOOTP(op=1, chaddr=src_mac) / DHCP(options=[('message-type', 'discover'), 'end'])
    sendp(pkt, iface="en0")
    print("SEND: Discover")


def receive_offer():
    print("RECEIVE: Offer")
    return sniff(iface="en0", filter="port 67",
                 stop_filter=lambda pkt: BOOTP in pkt and pkt[BOOTP].op == 2 and pkt[DHCP].options[0][1] == 2,
                 timeout=5)


def send_request(src_mac, request_ip, server_ip):
    pkt = Ether(dst='ff:ff:ff:ff:ff:ff', src=src_mac, type=0x0800) / IP(src='0.0.0.0', dst='255.255.255.255') / \
          UDP(dport=67, sport=68) / BOOTP(op=1, chaddr=src_mac) / \
          DHCP(options=[('message-type', 'request'), ("client_id", src_mac), ("requested_addr", request_ip),
                        ("server_id", server_ip), 'end'])
    sendp(pkt, iface="en0")
    print("RECEIVE: Acknowledge")


def receive_acknowledge():
    return sniff(iface="en0", filter="port 67",
                 stop_filter=lambda pkt: BOOTP in pkt and pkt[BOOTP].op == 2 and pkt[DHCP].options[0][1] == 5,
                 timeout=5)



# generate valid random MAC address:
def random_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
        random.randint(0, 255), random.randint(0, 255))


def run_dhcp_client():
    mac = random_mac()
    send_discover(mac)
    pkts = receive_offer()
    print(' #######################  \n\tDHCP DATA: \n  ####################### ')

    server_mac = pkts[0]["Ether"].src
    bootp_reply = pkts[0]["BOOTP"]
    server_ip = bootp_reply.siaddr
    offered_ip = bootp_reply.yiaddr
    dns_server = pkts[0][DHCP].options[2][1]

    print("OFFER IP:", offered_ip)
    print("DNS server IP: ", dns_server)
    print("SEND: Request for", offered_ip)
    
    send_request(mac, offered_ip, server_ip)
    pkts2 = receive_acknowledge()
    print("ACKNOWLEDGE:", offered_ip)

    return offered_ip, dns_server