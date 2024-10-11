## sections: Overview of Application, Client->VPN Server Message Format, VPN Server->Client Message Format, Example Output, **a description of how the network layers are interacting when you run your server, VPN server, and client**, and Acknowledgments.

### Overview of Application 
This is a VPN-Server application consisting of a client, a VPN, and a server. In short, the client takes in a data message from the user through command line, encodes the data message by adding a header with VPN IP, VPN Port, Server IP, and Server Port to the front, and sends that encoded message to the VPN. 

Then the VPN decodes the message and parses it to extracts the Server IP, Server Port, and data message. Then, without closing the socket of the client, the VPN opens a new socket to the server using the server IP and port, encodes the data message again, and sends the message to the server. 

The server receives and decodes the message and processes the data by performing the requested function. Then, it takes the processed message, encodes it, and sends it back to the VPN. The VPN also sends the data back to the client using the socket between VPN and client. 

Then the client will print out the received response, and the process is finished. 


### Client -> VPN Server Message Format 
First, the client will have to create a socket take an input from the command prompt. This could the a requested verb operation to tell the server how to process the data. Then, the client needs to encode the data to send the information to the VPN. The data is encoded in a function called encode_message, taking in the raw data as a parameter. During the encoding process, a header is added to the front of the data. The header includes the VPN IP, VPN Port, Server IP and Server port with spaces in between each information to separate the numbers. The header is a string and added to the string message. The message is sent to the VPN. 

The message format is MSG = VPN_IP VPN_Port SERVER_IP SERVER_PORT message. For example, 127.0.0.1 55554 127.0.0.1 65432 Ascending 12 -123 4.5 892 3.
VPN_IP = 127.0.0.1
VPN_PORT = 55554
SERVER_IP = 127.0.0.1
SERVER_PORT = 65432
Message = Ascending 12 -123 4.5 892 3

### VPN Server->Client Message Format
The VPN listens for a connection from the client. Then it receives the message from the client and parses the message in a function called parse_message with the client message as a parameter. During parse message, the message is decoded. Then the message is split by " " into a list so it can be easily extracted. The Server IP is the third element and the Server port is the fourth, so both of these information will be indexed into a saved variable. The message could be a sentence with spaces but was separated by space into a list, so we have to join the rest of the data together with a " " to ensure no data gets lost. 

Afterwards, the VPN connects to the server using the server IP and port it extracted and then it forwards only the message to the server. Then VPN waits for a response from the server to be forward back to the client. 

The VPN to client message format is the list of numbers sorted by the. For example, ['-123', '3', '4.5', '12', '892']. 


### Example Output / Command Line Trace 

## server trace
python sorting-server.py

server starting - connecting to server at IP 127.0.0.1 and port 65432

Server is binding to Host and Port

Listening for incoming connections...

Connected established with ('127.0.0.1', 51363)

Message received! 'b'Ascending 12 4.3 123 3.2 1''

Received client message: 'b'Ascending 12 4.3 123 3.2 1'' [26 bytes]

requested sorting operation is ascending

request includes  5  arguments: ['12', '4.3', '123', '3.2', '1']

sending result back to client:  ['1', '3.2', '4.3', '12', '123']

server is done!

## VPN trace

python VPN.py

VPN starting - connecting to client at IP 127.0.0.1  and port  55554

Connected established with ('127.0.0.1', 51361)

Received response from client: 'b'127.0.0.1 55554 127.0.0.1 65432 Ascending 12 4.3 123 3.2 1'' [58 bytes]

Parsing the message from the client...

creating a new socket and connecting to server at IP 127.0.0.1 and port 65432

connection established, sending message to server ' Ascending 12 4.3 123 3.2 1

message sent to server, waiting for echo response

Received response from server: '['1', '3.2', '4.3', '12', '123']' [32 bytes]

sending to client: '['1', '3.2', '4.3', '12', '123']'

VPN is done!

## client trace

python client.py

client starting - connecting to VPN at IP 127.0.0.1 and port 55554

connection established with VPN

Please input an operation or press Enter to quit: Ascending 12 4.3 123 3.2 1

sending message to VPN '127.0.0.1 55554 127.0.0.1 65432 Ascending 12 4.3 123 3.2 1'

message sent, waiting for reply

Received response: '['1', '3.2', '4.3', '12', '123']' [32 bytes]

client is done!


### Description of how network layers are interacting when the server, VPN, and client are running 
The layers in the TCP/IP model include Application layer, Transport layer, Network Layer, and Data link layer. 

The application layer is responsible for providing services to users. In this program, the application layer interacts with users by requesting them to input a message or operation and this occurs when the client asks the user for input. 

The transport layer uses the protocol TCP and sends an acknowledgement to the source computer to ensure that the data has successfully been received. In this program, this occurs when sending all the message over to the destination from the sources. For example, when the client is sending data to the VPN, the transport layer will ensure that the VPN has received the message and that the data does not have to be resent. After the acknowledgement, the client will delete its copy of the data. 

The network layer is where the router looks to see the destination IP and port. This occurs when data is sending from the source to the destination. For example, when the VPN is sending data to the destination, the server, the router searches for the IP and port to ensure the data is sending to the correct requested server. 

The link layer is responsible for deciding how to transmit the data from the client to the VPN to the server. Since this is wireless, the link layer is responsible for encoding the message to be understandable for the receiving end. When the server, client, and VPN are sending the message to each other, the link layer is behind the scenes, encoding the message for the destination to understand. The link layer also ensures the receiving end is successfully receiving the data and that when it is sending, there are no simultaneous data transmitting. 


### Acknowledgements 
I worked on this by myself. 