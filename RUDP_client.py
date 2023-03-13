# import:
import socket
import random

# consts:
fragment_size = 640
packet_size = 2048
# TODO(I): check for real fragment & packet size.


# start relable UDP connection:
def RUDP_connection(server_ip,user_ip,server_port):
    # Create UDP socket and establish connection
    UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP_socket.bind((user_ip, 20140))
    print ("\nConnecting to RUDP server %s:%s..." % (server_ip, server_port))
    return UDP_socket




# make shoure relable connection by three way handshack process
def handshake_process(UDP_socket, server_ip, server_port):

    # Step 1 (SYN)
    UDP_socket.sendto(bytes("SYN", encoding='utf8'), (server_ip, server_port))
    print ("Waiting for server response...\n\n")
    
    # Step 2 (SYN + ACK) 
    server_response = get_response(UDP_socket)
    if server_response == "SYN/ACK":
        # Step 3 (ACK)
        UDP_socket.sendto(bytes("ACK", encoding='utf8'), (server_ip, server_port)) 
        print("connection sucsseed!\n")        
        return True
    else:
        return False



def get_request(UDP_socket, server_ip, server_port, file_name):
    UDP_socket.sendto(bytes(file_name, encoding='utf8'), (server_ip, server_port))
    print("file name was sent waiting for server response...\n\n")

    server_response = get_response(UDP_socket)
    if server_response == "ACK":
        return True
    
    else:
        return False



"""
the function return list of packets organized by the sequence number 
"""
def receive_data_from_server(socket): #todo

    packet_recv = [] # the list

    count_of_seq=0 # hold how many packets recv

    #run as long the server sending packets
    while True:

        # wait for next packet from server:
        data, server_addr = socket.recvfrom(packet_size)

        # checking the data that recived: the first number is the seq-packet, the second is from how many, and the rest is the packet-data
        seq, num, packet = data.decode('utf-8').split(',', 2)
        seq = int(seq)
        num = int(num)
        count_of_seq += 1 # increasing the counter every time packets came

        print(f"packet {seq+1}/{num+1} resived!", end=" ")
        print("count_of_seq = ", count_of_seq - 1)

        # the client responds for every packet with "ACK" and seqence number of the corrent packet:
        ans = "ACK"
        socket.sendto(bytes(f"{ans},{seq}", encoding='utf8'), server_addr)

        # saving the packet in sequnse index in the list
        packet_recv.insert(seq, packet)

        # ending the loop when all packets came
        if count_of_seq >= num+1:
            print("\nlast ack received!")
            break

    return packet_recv # returning the list





def get_response(UDP_socket):
    try:
        rec_msg = UDP_socket.recvfrom(fragment_size)
        print ("Server response: %s" % rec_msg[0].decode('utf-8'))
        return rec_msg[0].decode('utf-8')
    except:
        return "TIMEOUT"




def four_way_handshack(UDP_socket, server_ip, server_port):
    print("\nclosing RUDP connection with server %s: %s." % (server_ip, server_port))

    # Step 1 (FIN)
    UDP_socket.sendto(bytes("FIN", encoding='utf8'), (server_ip, server_port))
    print("Waiting for server response...\n\n")

    # Step 2  (ACK)
    server_response = get_response(UDP_socket)
    if server_response == "ACK":
        # Step 3: (FIN)
        server_response = get_response(UDP_socket)
        if server_response == "FIN":
        
        # Step 4 (ACK)
            UDP_socket.sendto(bytes("ACK", encoding='utf8'), (server_ip, server_port))
            print("end of convesetion!\n")
        # Close socket
    
    print("Shutting down client.")
    UDP_socket.close()



