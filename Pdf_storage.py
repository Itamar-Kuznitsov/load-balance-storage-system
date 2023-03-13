# for tcp connection replace this import in the one below
from RUDP_Storage_server_interface import *
# from TCP_Storage_server_interface import *

# consts:
mp4_storage_ip = "127.0.0.1"
mp4_storage_port = 8880

files_dictionary ={
    "testP1.pdf": {"200": "./testP.pdf"},
    "testP2.pdf": {"200": "./testP.pdf"},
    "testP3.pdf": {"200": "./testP.pdf"},
    "testP4.pdf": {"200": "./testP.pdf"}
}



if __name__ == "__main__":   
    print("########    PDF_STORAGE SERVER IS OPEN    ###########") 
    storage_server(mp4_storage_ip, mp4_storage_port, files_dictionary)