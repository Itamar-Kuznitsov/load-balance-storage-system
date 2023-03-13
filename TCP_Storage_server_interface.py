# imports:
import socket
import time
import base64

# consts:
packet_buffer = 1024
Mp4_storage_port = 8881 
Pdf_storage_port = 8880 

# This function create a TCP server. receive user's file name and sending the file back to him 
def storage_server(server_ip, server_port, files_dictionary):
    # creating TCP connection on specific ip src
    TCP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_SOCKET.bind((server_ip, server_port))
    TCP_SOCKET.listen(5)
    print("\nTHIS IS THE TCP CONNECTION VESION")
    print("waiting for client")
    
    storage_server_port = 30632
    # stay open for receiving clients
    while True:
        client_sock, addr = TCP_SOCKET.accept()
    
        # receive the name of the file
        file_name = client_sock.recv(packet_buffer).decode('utf-8')
        # check the file on the server database, return status and the file data 
        status, payload = find_file_name(file_name, files_dictionary)
        # check for file type for redirection to the file type server
        file_type = list(file_name.split('.'))[1]
        
        
        # update the storage_server_port, each file_type server have a differante port: 
        if file_type == "mp4":
            storage_server_port = str(Mp4_storage_port)
        
        elif file_type == "pdf":
            storage_server_port = str(Pdf_storage_port)

        # send to user: request status, redirect to server port, file data(file/storage server ip):
        client_sock.send(status.encode('utf-8'))
        time.sleep(0.2)
        client_sock.send(storage_server_port.encode('utf-8'))
        time.sleep(0.2)
        packet_list = []
   
        if status == "200":
            packet_list = file_to_packets(payload)
            client_sock.send(str(len(packet_list)).encode(('utf-8')))
            time.sleep(0.2) 

            for item in packet_list:
                client_sock.send(str(item).encode('utf-8'))   
        
        elif status == "301":
            client_sock.send(str(payload).encode('utf-8'))       
    
            

        print("\nItem status: ", status)
        print("Payload have been sent")
        print ("\nClosing TCP connection")
        # close tcp connect
        client_sock.close()
        print ("\nFor closing TCP server socket press CTRL+C")


# 
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