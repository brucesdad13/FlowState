# Python program to implement server side of chat room.
import socket
import select
import sys
from _thread import *
import pickle
import ast

"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
delim = b'\x1E'
# takes the first argument from command prompt as IP address
IP_address = socket.gethostname()

# takes second argument from command prompt as port number
Port = 5069

"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind((IP_address, Port))
server.settimeout(10)

"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)

list_of_clients = []

def clientthread(conn, addr):
    print("client thread started")
    connectionOpen = True
    # sends a message to the client whose user object is conn
    #conn.send("Welcome to this chatroom!")
    buffer = b''
    while True:
        while True:
            try:
                buffer += conn.recv(1024)
                if delim in buffer:
                    delimIndex = buffer.find(delim)
                    frame = buffer[:delimIndex]
                    frame = ast.literal_eval(frame.decode("utf-8"))
                    print(frame)
                    print("FOUND THE END OF THE MESSAGE!!!!")
                    print("frame: "+str(frame))
                    broadcast(frame, conn)
                    buffer = buffer[delimIndex+1:-1]
                    print("remaining buffer = "+str(buffer))

            except Exception as e:
                print(e)
                connectionOpen = False
                break
        if(not connectionOpen):
            print("client unresponsive")
            remove(conn)
            break

"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def broadcast(message, connection):
    print("broadcast()")
    print(str(len(list_of_clients))+" clients connected")
    for client in list_of_clients:
        #if client!=connection:
        try:
            dataOut = str(message).encode("utf-8")+delim
            print("sending message to client: "+str(client.getpeername()[0])+": "+str(dataOut))
            client.send(dataOut)
        except Exception as e:
            print(e)
            client.close()
            # if the link is broken, we remove the client
            remove(client)

def remove(connection):
    print("remove()")
    print("disconnecting client: "+str(connection.getpeername()[0]))
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:

    """Accepts a connection request and stores two parameters,
    conn which is a socket object for that user, and addr
    which contains the IP address of the client that just
    connected"""
    try:
        print("waiting for new clients...")
        conn, addr = server.accept()

        """Maintains a list of clients for ease of broadcasting
        a message to all available people in the chatroom"""
        list_of_clients.append(conn)

        # prints the address of the user that just connected
        print(str(addr) + " connected")

        # creates and individual thread for every user
        # that connects
        start_new_thread(clientthread,(conn,addr))
    except:
        pass

conn.close()
server.close()
