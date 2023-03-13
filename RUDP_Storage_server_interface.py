# imports:
from RUDP_server import *
import time
import base64


# consts:
packet_buffer = 1024
Mp4_storage_port = 8881 
Pdf_storage_port = 8880 


def storage_server(server_ip, server_port, files_dictionary):
    RUDP_SOCKET = RUDP_connection(server_ip, server_port)
    handshake_status, client_addr = handshake_process(RUDP_SOCKET)
 
    packet_list = []
    storage_server_port = 30632

    if handshake_status:
        # receive the name of the file and send ACK for client
        file_name = client_request(RUDP_SOCKET)
        status, file_location = find_file_name(file_name, files_dictionary)
        file_type = list(file_name.split('.'))[1]
        # print(file_type)
        # print(status)

        if status == "200": 
            packet_list = file_to_packets(file_location)
        
        elif status == "301":
            packet_list.insert(0, file_location)

        else:
            print("Error: status is not valid.")
        # print(packet_list)

        # update the storage_server_port 
        if file_type == "mp4":
            storage_server_port = Mp4_storage_port
        
        elif file_type == "pdf":
            storage_server_port = Pdf_storage_port
            
        send_status(RUDP_SOCKET, client_addr[0], client_addr[1], status, storage_server_port)
        time.sleep(0.02)
        # packet_list = ["123456789","abcdefg","/m2 /2/ 12345"]
        send_data_to_client(client_addr, RUDP_SOCKET, packet_list)
        four_way_handshack(RUDP_SOCKET)

    else:
        pass

    print ("for closing RUDP socket press CTRL+C")



def find_file_name(file_name, files_dictionary):
    if file_name in files_dictionary:
        value = files_dictionary.get(file_name)
        status = list(value.keys())[0]
        file_location = value.get(status)
        return status, file_location
    
    else:
        None



# make packets list from the file:
def file_to_packets(file_path):
    packets_list = []
    with open(file_path, "rb") as f:
        data = base64.b64encode(f.read(packet_buffer))

        while(data):
            packets_list.append(data)
            data = base64.b64encode(f.read(packet_buffer))
            
        f.close()
    return packets_list
