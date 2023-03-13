import socket

dns_server_ip = '8.8.8.8'
host = ''
port = 53
backlog = 5
size = 1024


"""
ABOUT:
    this program is the server side of local DNS server.
    As we learn, local DNS has local cache of recent name-to-address
    translation pairs (but maybe out of date!).
    it is acts as proxy.

"""

# dictionary that represent the local DNS "name-to-address translation pairs"
local_cache = {
    "www.google.com": "12.154.254.33",
    "www.myApp.com": "127.0.0.1",
    "www.ynet.com": "127.0.0.2",
    "www.appstore.com" : "127.0.0.1"
}


# check if the domain we locking for is in the local DNS
def check_local_cache(domain):
    if domain in local_cache:
        ip_address = local_cache.get(domain)
    else:
        try:
            ip_address = socket.gethostbyname(domain)
        except socket.gaierror:
            return None
        local_cache[domain] = ip_address
    return ip_address




def local_DNS_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(backlog)
    print("waiting for client")

    while True:
        sock_client, address = s.accept()
        recv_domain = sock_client.recv(size)
        domain = recv_domain.decode('utf-8')
        ap_ip= check_local_cache(domain)

        encode_ip=ap_ip.encode('utf-8')
        sock_client.send(encode_ip)
        for key in local_cache:
            print(key)
        break
    
    sock_client.close()
    s.close()
        
        

if __name__ == "__main__":
    print("########    DNS SERVER IS OPEN    ###########")
    local_DNS_server()