# Simulation to load-balance storage system based on custom RUDP / TCP connection 

## Description

This is a smart storage server system based on load balancing and HTTP redirection.

* The user connects to the network and receives a local address from the DHCP server.

* Then the user turns to the local DNS server and receives the address of the main storage server - App Store
which directs us by using redirection and through load routing logic to the dedicated server that stores the requested file.

* The user turns to this server and receives back the file he requested for the computer.
This is how we created a server system that allows storing and downloading files efficiently and supports loads.

There are two different possible types of connection: custom RUDP(reliability/Congestion Control/Flow Control) & TCP   

## In the future

This storage server system is based on load balancing and supports downloading files of the type: 
pdf and mp4 when the system can be expanded very easily since it is a generic system.

This is a simulation of a system that can withstand a high scale in the real world where 
we use redirecting servers to a server that knows how to handle the type of request.
The servers in the future will be able to handle unique requests and be clustered in different ways
so that it can be taken a few steps further in the future.


## About
This RUDP conneection is based on 3 main abilities:
* Reliability - opening and closing a connection in a controlled manner, 
  based on the principles of TCP 3-Way Handshake Process and 4 way handshake.
  
* Congestion Control - load control in the transmission of information in the network, 
  based on Reno congestion control and fast retransmit.
  
* Flow Control - control of receiving/sending information and losing packets, 
  for good data flow based on the principles of Selective Repeat and Stop & wait.



## Executing program
First, download the files above to your local machine. 

Run the Servers on different terminals/ containers/ VM:
```
python3 DHCP_Server.py
python3 DNS_Server.py
python3 App_store.py
python3 Mp4_storage.py
python3 Pdf_storage.py
```
And then run the User:

For RUDP connection:
```
 python3 RUDP_User.py
```

For TCP connection:
```
 python3 TCP_User.py
```

Made by

* [Itamar Kuznitsov](https://github.com/Itamar-Kuznitsov)

## Version
* 0.1
  * Initial release ~ March 2023
