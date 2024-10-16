#!/usr/bin/env python3

import socket
import arguments
import argparse

# Run 'python3 client.py --help' to see what these lines do
parser = argparse.ArgumentParser('Send a message to a server at the given address and print the response')
parser.add_argument('--server_IP', help='IP address at which the server is hosted', **arguments.ip_addr_arg)
parser.add_argument('--server_port', help='Port number at which the server is hosted', **arguments.server_port_arg)
parser.add_argument('--VPN_IP', help='IP address at which the VPN is hosted', **arguments.ip_addr_arg)
parser.add_argument('--VPN_port', help='Port number at which the VPN is hosted', **arguments.vpn_port_arg)
parser.add_argument('--message', default=['Hello, world'], nargs='+', help='The message to send to the server', metavar='MESSAGE')
args = parser.parse_args()

SERVER_IP = args.server_IP  # The server's IP address
SERVER_PORT = args.server_port  # The port used by the server
VPN_IP = args.VPN_IP  # The server's IP address
VPN_PORT = args.VPN_port  # The port used by the server
MSG = ' '.join(args.message) # The message to send to the server

def encode_message(message):
    ''' 
    Encode the message by adding a header with information about VPN IP/PORT and SERVER IP/PORT
    Return the message with header to the message.
    '''
    # Add an application-layer header to the message that the VPN can use to forward it
    #header includes VPN_IP, VPN_Port, SERVER_IP, SERVER_PORT
    app_header = str(VPN_IP) + " " + str(VPN_PORT) + " " + str(SERVER_IP) + " " + str(SERVER_PORT)

    #attach the header to the message
    message = app_header + " " + message

    return message


print("client starting - connecting to VPN at IP", VPN_IP, "and port", VPN_PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((VPN_IP, VPN_PORT)) #connecting to the VPN IP and Port
    print("connection established with VPN")
    
    #encoding the message by adding a header with VPN/Server Ip and Port
    #input = input("Please type in the kind of sorting you want to perform AND the list of numbers to sort: \n-Ascending \n-Descending\n-Enter to exit\n")
    inp = input("Please input an operation or press Enter to quit: ")
    MSG = encode_message(inp) #encode the message 
    print(f"sending message to VPN '{MSG}'")
    s.sendall(bytes(MSG, 'utf-8')) #sending the message to the VPN
    print("message sent, waiting for reply")
    data = s.recv(1024).decode("utf-8") #receiving the message from the server and decoding it
    print(f"Received response: '{data}' [{len(data)} bytes]") # printing the received response from the VPN
    
 #received response from the server.
print("client is done!")
