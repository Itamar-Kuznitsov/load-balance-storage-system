import socket

dns_server_port = 53
size = 1024

def get_domain_local_dns(dns_server,query):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((dns_server,dns_server_port))
    encode_ip = query.encode('utf-8')
    s.send(encode_ip)
    recive_add = s.recv(size)
    ip_address = recive_add.decode('utf-8')
    s.close()
    print(' #######################  \n\tDNS DATA: \n  ####################### ')
    print(query, "ip address is: \t", ip_address)
    return ip_address

