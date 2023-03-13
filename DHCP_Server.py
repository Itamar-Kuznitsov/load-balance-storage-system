# import:
from scapy.all import *
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether
from scapy.layers.dhcp import *


#input info
server_ip='127.0.0.1'
client_ip='127.0.0.1'
server_mac="00:0B:CD:AE:9F:C6"
client_mac="00:02:a5:ea:54:20"
subnet_mask="255.255.255.192"
dns_servers = '127.0.0.1'
gateway="12.154.254.10"


def receive_discover():
    sniff(filter="udp port 68",
            stop_filter= lambda pkt: pkt[DHCP] and pkt[DHCP].options[0][1] == 1, prn=send_offer, store=0)


# send DHCP Offer to client:
def send_offer(pkt):
    print("received DHCP discover :")
    offer_pkt = Ether(src=server_mac,dst="ff:ff:ff:ff:ff:ff")/\
                IP(src=server_ip,dst="255.255.255.255")/\
                UDP(sport=67,dport=68)/\
                BOOTP(
                    op=2,
                    yiaddr=client_ip,
                    siaddr=server_ip,
                    giaddr=gateway,
                    chaddr=client_mac,
                    xid=pkt[BOOTP].xid
                )/\
                DHCP(options=[('message­type','offer')])/\
                DHCP(options=[('subnet_mask',subnet_mask)])/\
                DHCP(options=[('domain',dns_servers)])/\
                DHCP(options=[('server_id',server_ip),('end')])
    sendp(offer_pkt, iface="en0")
    print ("DHCP Offer packet sent\n.")
        

def receive_request():
    sniff(filter="udp port 68", stop_filter= lambda pkt: DHCP in pkt and pkt[DHCP].options[0][1]== 3, prn=send_acknowledge, store=0)


def send_acknowledge(pkt):

    print ("DHCP Request packet detected")
    sendp(
        Ether(src=server_mac,dst="ff:ff:ff:ff:ff:ff")/
        IP(src=server_ip,dst="255.255.255.255")/
        UDP(sport=67,dport=68)/
        BOOTP(
            op=2,
            yiaddr=client_ip,
            siaddr=server_ip,
            giaddr=gateway,
            chaddr=client_mac,
            xid=pkt[BOOTP].xid
        )/
        DHCP(options=[('message­type','offer')])/\
        DHCP(options=[('subnet_mask',subnet_mask)])/\
        DHCP(options=[('domain',dns_servers)])/\
        DHCP(options=[('server_id',server_ip),('end')]))
    
    print ("DHCP Ack packet sent\n\nCtrl+C to exit\n")
    
        



if __name__ == "__main__":
    print("########    DHCP SERVER IS OPEN    ###########")
    receive_discover()
    
    receive_request()


