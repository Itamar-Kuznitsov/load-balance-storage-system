# imports:
import socket
from DHCP_Client import *
from DNS_Client import *
import base64
import time

# const:
app_store_port = 30632
user_port = 20140
query = "www.appstore.com"
file_name = "Butterfly2.mp4" #"testP2.pdf" #
packet_list = []
payload = None

# Send file request by TCP:
def request_file(server_ip, server_port, user_port, file_name):
    # creating TCP connection on a spesific ip src
    TCP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_SOCKET.bind((user_ip, user_port))
    TCP_SOCKET.connect((server_ip,server_port))
    
    # file request from the server
    request_status = TCP_SOCKET.send(file_name.encode('utf-8'))
    
    if request_status:    
        # receiving the file status
        status = TCP_SOCKET.recv(1024).decode('utf-8')
        time.sleep(0.2)
        # receiving the storage server port which we should connect to
        storage_server_port = TCP_SOCKET.recv(1024).decode('utf-8') 
        time.sleep(0.2)

        if status == "200":
            packet_len = TCP_SOCKET.recv(1024).decode('utf-8')
            time.sleep(0.2)
            for i in range(int(packet_len)):
                data = TCP_SOCKET.recv(4096).decode('utf-8')
                packet_list.append(data)
            time.sleep(0.2)


        elif status == "301":
            # receiving the payload: storage_server ip or the file itself.
            payload = TCP_SOCKET.recv(4096).decode('utf-8')
            time.sleep(0.2)

        print("Request status: ", status)
        return status, payload, packet_list, int(storage_server_port)
    
    else:
        print("Error: sending file_name to server has been failed")

# saving the payload from the server localy in custom file, return the file name was created
def packet_to_file(payload, file_name):
    f = open(file_name, 'wb')
    data = "".join(payload)
    
    padding = b'=' * (4 - len(data) % 4)
    binary_data = base64.b64decode(data + padding.decode('utf-8'))
    f.write(base64.b64decode(binary_data))
    f.close()
    return file_name


# the main function that call the right function based on the system logic:
def main(status, storage_server_port, payload, packet_list):
    # if the file in the server:
    if status == "200":
        print("file found!")
        return status, packet_to_file(packet_list, file_name)
    
    # if the file is in another server:
    elif status == "301":
        print("Redirect to: ",payload, storage_server_port)
        status, payload, packet_list, server_p = request_file(payload, storage_server_port, user_port, file_name)
        return status, packet_to_file(packet_list, file_name)   
    
    # status error:
    else:
        print("status not valid!")




if __name__ == "__main__":
    # Some documentation about the system 
    print('###########################################################\n###########################################################\
            \n############# WELCOME TO THE APP_STORE SYSTEM #############\n###########################################################\
            \n###########################################################')
    print("\nThe APP STORE system is a smart, efficient & load balance file storage place")
    print("\nFor downloading the file from the storage system you need to update the")
    print("file name in the constant area. \n")
    
    print("ABOUT THE ARICTACTURE: we made main server called APP_STORE which make a redirection")
    print("\t\t\tfor the right server that responsible for storaging spesific")
    print("\t\t\tspesific type of files such as: pdf, mp4 etc.\n") 
    
    print("\nThis version is based TCP connection")
    print("\nMade by: Shachar ketz & Itamar Kuznitsov.")
    print("\nVersion: 1.0  -  March. 2023")

    user_ip, dns_server = run_dhcp_client()
    app_store_ip = get_domain_local_dns(dns_server, query)
    # open connection with App_store to get the storage address.
    status, payload, packet_list, storage_server_port = request_file(app_store_ip, app_store_port, user_port, file_name)
    status, file = main(status, storage_server_port, payload, packet_list)
    print('\n\nTHERE YOU GO, YOUR FILE IS NOW IN YOUR LOCAL MACHINE')
    print(' ###########################################################')
    print('\t\t', status, file)
    print(' ###########################################################')


