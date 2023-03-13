from RUDP_client import *
from DHCP_Client import *
from DNS_Client import *
import base64


# const:
app_store_port = 30632
user_port = 20140
query = "www.appstore.com"
file_name = "Butterfly2.mp4" #"testP2.pdf" #



# send file request by RUDP
def request_file(server_ip, server_port, user_port, file_name):
    RUDP_SOCKET = RUDP_connection(server_ip, user_ip, user_port)
    handshack_status = handshake_process(RUDP_SOCKET, server_ip, server_port)
    
    if handshack_status:
        # ask for the file from the server
        request_status = get_request(RUDP_SOCKET, server_ip, server_port, file_name)
        
        if request_status:    
            status, storage_server_port = get_response(RUDP_SOCKET).split(',')
            print(status)
            print(storage_server_port)
            payload = receive_data_from_server(RUDP_SOCKET)
           
            four_way_handshack(RUDP_SOCKET, server_ip, server_port)
            return status, payload, int(storage_server_port)

    else:
        pass


def packet_to_file(payload, file_name):
    f = open(file_name, 'wb')
    data = "".join(payload)
    
    padding = b'=' * (4 - len(data) % 4)
    binary_data = base64.b64decode(data + padding.decode('utf-8'))
    f.write(base64.b64decode(binary_data))
    f.close()
    return file_name



def main(status, storage_server_port, payload):
    # if the file in the server:
    if status == "200":
        print("file found!")
        return status, packet_to_file(payload, file_name)
    
    # if the file alocate in another server:
    elif status == "301":
        print("Redirect to: ",payload[0], storage_server_port)
        status, payload, server_p = request_file(payload[0], storage_server_port, user_port, file_name)
        # print(status)
        # print(payload)
        return status, packet_to_file(payload, file_name)   
    
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
    
    print("\nThis version is based RUDP connection")
    print("\nMade by: Shachar ketz & Itamar Kuznitsov.")
    print("\nVersion: 1.0  -  March. 2023")


    user_ip, dns_server = run_dhcp_client()
    app_store_ip = get_domain_local_dns(dns_server, query)
    # open connection with App_store to get the storage address.
    status, payload, storage_server_port = request_file(app_store_ip, app_store_port, user_port, file_name)
    status, file = main(status, storage_server_port, payload)
    print('\n\nTHER YOU GO, YOUR FILE IS NOW IN YOUR LOCAL MACHINE')
    print(' ###########################################################')
    print('\t\t\t', status, file)
    print(' ###########################################################')


