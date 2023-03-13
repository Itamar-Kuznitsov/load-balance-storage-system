# import:
import socket
import sys

# consts:
fragment_size = 640
client_list = []



# start relable UDP connection:
def RUDP_connection(ip, port):
    # Create UDP socket and bind it to IP address and port
    UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP_socket.bind((ip, port))
    print ("** RUDP SERVER  ** on %s: %s\n\n" % (ip, port))
    print ("Waiting for client...\n\n")

    return UDP_socket

    


# make shoure relable connection by three way handshack process
def handshake_process(UDP_socket):

    # Listen to socket
    msg, client_addr = UDP_socket.recvfrom(fragment_size)
    msg = msg.decode('utf8')
    print("Message received from %s: %s: \n" % (client_addr[0], client_addr[1]) + msg)

    # Step 1 (SYN) - Establish connection
    if msg == "SYN":
        client_list.append(client_addr)  # Add client to list (authorisation)

        #  Step 2 (SYN + ACK) 
        UDP_socket.sendto(bytes("SYN/ACK",encoding='utf8'), client_addr)  # Send ACK to confirm connection
        print ("Connection established with %s:%s!\n" % (client_addr[0], client_addr[1]))
    
    else:
        UDP_socket.sendto(bytes("NACK", encoding='utf8'), client_addr)  # Reject client
        print ("Authentication failed! Client must first establish connection with server.")
        return False, client_addr
        
    # Listen to socket
    msg, client_addr = UDP_socket.recvfrom(fragment_size)
    msg = msg.decode('utf8')
    print ("Message received from %s:%s: \n" % (client_addr[0], client_addr[1]) + msg)
    
    # Step 3 (ACK)
    if msg == "ACK":
        # Authentication process -  prevent unauthorised clients from getting data and ack spoofing attack
        if client_addr in client_list:
            print("\nAuthentication confirmed.\n")
            return True, client_addr
        else:
            pass

    else:
        UDP_socket.sendto(bytes("NACK", encoding='utf8'), client_addr)  # Reject client
        print ("Authentication failed! Client must first establish connection with server.")
        return False, client_addr



# send the request status tothe client: 200- the server have the file. 301- redirect.
def send_status(UDP_socket, client_ip, client_port, status, storage_server_port):
    UDP_socket.sendto(bytes(f"{status},{storage_server_port}", encoding='utf8'), (client_ip, client_port))




# send the data via our RUDP connection
def send_data_to_client(client_addr, UDP_socket, packets_list):
    packet_size = 1024                      # size of ack packet
    cwnd = 1                                # size of sending window
    num_of_packets = len(packets_list)      # how many packet to send
    TIMEOUT = 2                             # time out for ack- TTL
    SS_flag = True                          # the parameter for cwnd growing
    problem = False                         # the client and server dont anderstend each other
    Threshold = sys.maxsize                 # holds the superiors value- cwnd is bigger then Threshold, we change to AI-growing
    ack_list = [False]*(num_of_packets)     # the list holds True in index 'i', if the acknolage packet receved for packet sequence 'i'
    seq_num = 0                             # hold the indexs for the first packet in cwnd
    ack_num = 0                             # hold the next position for seq_num
    num_of_acks=0                           # counter how many packets the client got


    # the loop is sending packets and resiving ack's until client got all packets or error
    while (not problem) and (num_of_acks < num_of_packets):

        # RESET FLAGS:
        lost_packets_flag = False
        sending_packets_flag = False # had server sent packet from this cwnd?

        # sending packets in the cwnd:
        for i in range(seq_num, min(seq_num + cwnd, len(packets_list))):

            # only if the client didn't got the packet:
            if ack_list[i] == False:

                sending_packets_flag = True
                UDP_socket.sendto(bytes(f"{i},{num_of_packets-1},{packets_list[i]}", encoding='utf-8'), client_addr)
                print(f"Sent packet {i}/{num_of_packets-1}")
            else:
                print("packets ",i ,"already had sent!")


        # Wait for ACK's from client:
        if sending_packets_flag:
            for i in range(seq_num, min(seq_num + cwnd, len(packets_list))):

                # wait only for ack of sent packets:
                if ack_list[i] == False:

                    # TTL for each packet:
                    UDP_socket.settimeout(TIMEOUT)

                    try:
                        # each acknolage packets holds ans-"ACK", and sequence_num_of_ack
                        data, addr = UDP_socket.recvfrom(packet_size)
                        ans, sequence_num_of_ack = data.decode('utf-8').split(',')

                        # increase the counter:
                        num_of_acks += 1

                        if ans == "ACK":
                            sequence_num_of_ack = int(sequence_num_of_ack)

                        # ERROR!
                        else:
                            print("unknown acknowledge!")
                            problem = True
                            break

                        # save in the list of ack's that we got ack for the sequence_num_of_ack
                        ack_list[sequence_num_of_ack] = True
                        print("Received ACK", sequence_num_of_ack)

                        ack_num = sequence_num_of_ack+1 # next packet without ack

                    # TIME OUT! packet lost
                    except socket.timeout:

                        print("Timeout, packets lost:")
                        lost_packets_flag = True
                        first_false_ack_flag = True

                        #find first lost packet in the list
                        for i in range(0, min(seq_num + cwnd, len(packets_list))):
                            if ack_list[i] == False:
                                print( i ,end=" ") #list of lost packets
                                print(" ",i)
                                if first_false_ack_flag:
                                    ack_num = i
                                    first_false_ack_flag = False
                        print("\n restart cwnd from packet ",ack_num)
                        print("cwnd =",cwnd)

                        # RESET cwmd:
                        Threshold = max(1,cwnd//2)          # half of cwnd
                        cwnd = 1                            # restart cwnd
                        seq_num = ack_num                   # first packet in cwnd is the first lost packet
                        print("seq num= ",seq_num)
                        SS_flag = True                      # cwnd grow in exponentially way
                        break


        else: # if sending_packets_flag is False:
            # find first
            for i in range(seq_num, len(packets_list)):
                if ack_list[i] == False:
                    # first packet in cwnd is the first lost packet
                    print("next packet to send is ",i)
                    seq_num=i
                    break


        # update cwnd if no packet has lost:
        if lost_packets_flag is False:
            SS_flag, cwnd, seq_num, Threshold,flag = congection_control(SS_flag,cwnd,ack_num,Threshold,len(packets_list))
            if flag == False:
                print("error in the program!")
                break



    print("Finnish sending all packets!")



# RUDP congection control, based on RENO
def congection_control(SS_flag,cwnd,ack_num,Threshold, packet_list_size):

    if (SS_flag):
        cwnd *= 2
        seq_num = ack_num

    else:  # AI:
        cwnd += 1
        seq_num = ack_num

    # update SS_flag:
    if (cwnd >= Threshold):
        Threshold = cwnd
        SS_flag = False
    print("cwnd= ",cwnd)
    flag=True
    if cwnd > packet_list_size:
        flag=False
    return SS_flag, cwnd, seq_num,  Threshold, flag




#closing connection with the RUDP four way handshack
def four_way_handshack(UDP_socket):
    msg, client_addr = UDP_socket.recvfrom(fragment_size)
    msg = msg.decode('utf8')
    print("Message received from %s: %s: \n" % (client_addr[0], client_addr[1]) + msg)
    # Step 1 (SYN) - Establish connection
    if msg == "FIN":
        #  Step 2 (SYN + ACK)
        UDP_socket.sendto(bytes("ACK", encoding='utf8'), client_addr)  # Send ACK to confirm connection
        UDP_socket.sendto(bytes("FIN", encoding='utf8'), client_addr)  # Send ACK to confirm connection
        print("closing operetion with %s:%s!\n" % (client_addr[0], client_addr[1]))

    else:
        UDP_socket.sendto(bytes("NACK", encoding='utf8'), client_addr)  # Reject client
        print("Authentication failed!")
        client_list.remove(client_addr)  # Remove client from list
        return False

    # Listen to socket
    msg, client_addr = UDP_socket.recvfrom(fragment_size)
    msg = msg.decode('utf8')
    print("Message received from %s:%s: \n" % (client_addr[0], client_addr[1]) + msg)

    # Step 3 (ACK)
    if msg == "ACK":
        # Authentication process -  prevent unauthorised clients from getting data
        client_list.remove(client_addr)  # Remove client from list
        print("\nfinish conection!.\n")
        return True

    else:
        UDP_socket.sendto(bytes("NACK", encoding='utf8'), client_addr)  # Reject client
        print("Authentication failed!")
        client_list.remove(client_addr) # Remove client from list
        return False



# wait for client request
def client_request(UDP_SOCKET):
    file_name, client_addr = UDP_SOCKET.recvfrom(fragment_size)
    if client_addr in client_list:
        file_name = file_name.decode('utf-8')
        print("Message received from %s: %s: \n" % (client_addr[0], client_addr[1]) + file_name)
        
        UDP_SOCKET.sendto(bytes("ACK", encoding='utf8'), client_addr)
        return file_name
    else:
        print("Authentication failed! Client must first establish connection with server.")
        return None
    


