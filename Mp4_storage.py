# for tcp connection replace this import in the one below
from RUDP_Storage_server_interface import *
# from TCP_Storage_server_interface import *

# consts:
mp4_storage_ip = "127.0.0.1"
mp4_storage_port = 8881

files_dictionary ={
    "Butterfly1.mp4": {"200": "./testV.mp4"},
    "Butterfly2.mp4": {"200": "./testV.mp4"},
    "Nature1.mp4": {"200": "./testV.mp4"},
    "Nature2.mp4": {"200": "./testV.mp4"}
}




if __name__ == "__main__":    
    print("########    MP4_STORAGE SERVER IS OPEN    ###########")
    storage_server(mp4_storage_ip, mp4_storage_port, files_dictionary)