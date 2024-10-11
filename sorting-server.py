# This is a test server to test if the client and VPN work (extracted from Project 1 RPC APP.)
import socket 


HOST = "127.0.0.1" #Host Address
PORT = 65432 #port number

def decode_message(data, c): 
    '''
    Decodes the message, computes the request, and sends back to client

    Args: Encoded data to be decoded
    c: server socket
    '''
    print (f"Received client message: '{data!r}' [{len(data)} bytes]")
    decoded_data = data.decode('utf-8').strip() #decodes the data and strips any trailing/leading whitepaces
    number_list = decoded_data.split(" ") #Splits the data by spaces into a list
    number_list = [item.lower() for item in number_list] #lowercase the items in list to be processed despite case

    if "ascending" in number_list: 
        print("requested sorting operation is ascending")
        number_list.remove("ascending") #remove ascending command from the list of numbers 
        print("request includes ", str(len(number_list)), " arguments: " + str(number_list))
        number_list.sort(key=float) #sort the list of numbers as keys in ascneding order 
        response = str(number_list)

    elif "descending" in number_list: 
        print("requested sorting operation is descending")
        number_list.remove("descending") #remove descending command from the list of numbers 
        print("request includes ", str(len(number_list)), " arguments: " + str(number_list))
        number_list.sort(key=float, reverse = True) #sort the list of numbers as keys in descneding order 
        response = str(number_list)

    else: 
        print("Invalid Operation/Spelling. Try Again.")
        response = "Invalid Operation/Spelling."
    
    print("sending result back to client: ", response)
    c.sendall(bytes(response, 'utf-8')) #Send the sorted list as string as encoded data back to the client. 
    
def main(): 
    print("server starting - connecting to server at IP", HOST, "and port", PORT)

    #setting up the socket 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        print("Server is binding to Host and Port")
        s.bind((HOST, PORT)) #binding the host and port to the socket
        print("Listening for incoming connections...")
        s.listen()  #listening for incoming connections 
        conn, addr = s.accept() #connection accepted 

    with conn: 
        print(f"Connected established with {addr}") #connection established 
        MSG = conn.recv(1024) #message received from the client
        print(f"Message received! '{MSG}'")
        decode_message(MSG, conn) #decode the message 

    print ("server is done!")

if __name__ == "__main__": 
    main()