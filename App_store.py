# for tcp connection replace this import in the one below
from RUDP_Storage_server_interface import *
# from TCP_Storage_server_interface import *

# consts:
app_store_ip = "127.0.0.1"
app_store_port = 30632

files_dictionary ={
    "Butterfly1.mp4": {"200": "./Butterfly1.mp4"},
    "Butterfly2.mp4": {"301": "127.0.0.1"},
    "testP1.pdf": {"200": "./testP.pdf"},
    "testP2.pdf": {"301": "127.0.0.1"}
}




if __name__ == "__main__":    
    print("########    APP_STORE SERVER IS OPEN    ###########")
    storage_server(app_store_ip, app_store_port, files_dictionary)