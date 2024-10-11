#!/usr/bin/env python3

import socket
import arguments
import argparse
from arguments import _ip_address
from arguments import _port

# Run 'python3 VPN.py --help' to see what these lines do
parser = argparse.ArgumentParser('Send a message to a server at the given address and prints the response')
parser.add_argument('--VPN_IP', help='IP address at which to host the VPN', **arguments.ip_addr_arg)
parser.add_argument('--VPN_port', help='Port number at which to host the VPN', **arguments.vpn_port_arg)
args = parser.parse_args()

VPN_IP = args.VPN_IP  # Address to listen on
VPN_PORT = args.VPN_port  # Port to listen on (non-privileged ports are > 1023)

def parse_message(message):
    '''
    Takes the message from the client and parses the Server IP, Server port and message into variables
    '''
    message = message.decode("utf-8") #decode the message

    # Parse the application-layer header into the destination SERVER_IP, destination SERVER_PORT,
    # and message to forward to that destination
    split_data = message.split(' ') #split the String data by ' ' into a list
    SERVER_IP = split_data[2] #server IP is the third element in the list

    SERVER_PORT = int(split_data[3]) #server port is the fourth element in the list, converts it to an int
    message = ' '.join(split_data[4:]) #Rejoin the remaining elements from the list into a string

    return SERVER_IP, SERVER_PORT, message

### INSTRUCTIONS ###
# The VPN, like the server, must listen for connections from the client on IP address
# VPN_IP and port VPN_port. Then, once a connection is established and a message recieved,
# the VPN must parse the message to obtain the server IP address and port, and, without
# disconnecting from the client, establish a connection with the server the same way the
# client does, send the message from the client to the server, and wait for a reply.
# Upon receiving a reply from the server, it must forward the reply along its connection
# to the client. Then the VPN is free to close both connections and exit.

# The VPN server must additionally print appropriate trace messages and send back to the
# client appropriate error messages.

print("VPN starting - connecting to client at IP", VPN_IP, " and port ", VPN_PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    #binds to VPN IP and VPN Port
    s.bind((VPN_IP, VPN_PORT))
    #listens for the client
    s.listen()
    #accepts connection with client
    conn, addr = s.accept()

    with conn: 
        print(f"Connected established with {addr}")
        #while True: 
        client_data = conn.recv(1024)
        print(f"Received response from client: '{client_data}' [{len(client_data)} bytes]")

            # if not client_data:
            #     break    
        print("Parsing the message from the client...")
        SERVER_IP, SERVER_PORT, MSG = parse_message(client_data)
    
        print("creating a new socket and connecting to server at IP", SERVER_IP, "and port", SERVER_PORT)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as o:
            o.connect((SERVER_IP, SERVER_PORT)) #connect the socket to the server ip and port
            print(f"connection established, sending message to server ' {MSG}")
            o.sendall(bytes(MSG, 'utf-8')) #encode the parsed message and send to the server
            print("message sent to server, waiting for echo response")
            server_data = o.recv(1024).decode('utf-8') #receive the data from the server and decode the data
            print(f"Received response from server: '{server_data}' [{len(server_data)} bytes]")
            print(f"sending to client: '{server_data}'")
            conn.sendall(bytes(server_data, 'utf-8')) #Sending the data from the server to the client using the outer socket
    
    print("VPN is done!")
    


