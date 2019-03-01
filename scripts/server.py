import socket
import select
import sys
import pickle
import ast
import FSNObjects
import traceback
import time
import platform
import threading
import copy

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
delim = b'\x1E'
# takes the first argument from command prompt as IP address
IP_address = "0.0.0.0"#socket.gethostname()

# takes second argument from command prompt as port number
port = 50001

serverName = "noobs only"

"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
print("binding to "+str(IP_address)+":"+str(port))
server.bind((IP_address, port))


"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)

clientStates = {}
clientConnections = {}
outboundMessages = []

def clientThread(conn, addr):
    connectionOpen = True
    # sends a message to the client whose user object is conn
    #conn.send("Welcome to this chatroom!")
    lastRecv = time.time()
    buffer = b''
    while True:
        while True:
            try:
                buffer += conn.recv(1)
                if delim in buffer:
                    delimIndex = buffer.find(delim)
                    frame = buffer[:delimIndex]
                    frame = ast.literal_eval(frame.decode("utf-8"))
                    lastRecv = time.time()
                    #print("FOUND THE END OF THE MESSAGE!!!!")
                    #print("frame: "+str(frame))
                    messageType = frame[FSNObjects.MESSAGE_TYPE_KEY]
                    buffer = buffer[delimIndex+1:-1]
                    #print("remaining buffer = "+str(buffer))

                    #a player is sending an event
                    if messageType == FSNObjects.PLAYER_EVENT:
                        message = FSNObjects.PlayerEvent.getMessage(frame)
                        
                        
                        #a new player is joining the game
                        if(message.eventType==FSNObjects.PlayerEvent.PLAYER_JOINED):
                            print("player joined")
                            print(message)
                            #event = FSNObjects.ServerState(clientStates)
                            #send(event,conn)
                            clientStates[message.senderID] = {}
                            clientConnections[message.senderID] = {"socket":conn}
                            #let's let him know the state of the game
                            serverState = FSNObjects.ServerState(clientStates)
                            send(serverState,conn)
                            #let's associate the player state with this socket
                            print(clientStates)
                            for key in clientStates:
                                clientSocket = clientConnections[key]['socket']
                                if(clientSocket == conn):
                                    clientStates[key]['senderID'] = message.senderID
                            #let's let the new player know the state of the game
                            
                        if(message.eventType==FSNObjects.PlayerEvent.PLAYER_QUIT):
                            print("player quit: "+str(message.senderID))
                            remove(conn)
                            connectionOpen = False

                        if(message.eventType==FSNObjects.PlayerEvent.PLAYER_MESSAGE):
                            print("player sent game message :"+str(message.extra))
                            send(message, conn)


                    #a player is sending an update about their current state
                    if messageType == FSNObjects.PLAYER_STATE:
                        #print("Got a player state. Updating client states")
                        message = FSNObjects.PlayerState.getMessage(frame)
                        senderID = message.senderID
                        newClientState = frame
                        clientStates[senderID] = newClientState
                        clientConnections[senderID]['socket'] = conn
                        #print(clientStates)
                        #let the client know they can send more data


                    if(frame!=None):
                        sendAck(conn)
                        broadcast(frame, conn)
                        time.sleep(0.05)

            except Exception as e:
                print(traceback.format_exc())
                remove(conn)
                connectionOpen = False
                break
        if(not connectionOpen):
            print("client thread ending")
            break

"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def sendAck(socket):
    #print("sending ack to "+str(socket.getpeername()))
    ack = FSNObjects.ServerEvent(FSNObjects.ServerEvent.ACK)
    send(ack,socket)

def broadcast(message, socket):
    #print("broadcast()")
    try:
        for key in clientConnections:
            clientSocket = clientConnections[key]['socket']
            if clientSocket!=socket:
                send(message,clientSocket)
    except:
        pass

def send(message, socket):
    #print("send()")
    #global outboundMessages

    #outboundMessages.append({"data":message,"socket":socket})
    try:
        dataOut = str(message).encode("utf-8")+delim
        #print("sending message to client: "+str(socket.getpeername()[0])+": "+str(dataOut))
        socket.send(dataOut)
    except Exception as e:
        print(traceback.format_exc())
        #socketsToDisconnect.append(socket)
        socket.close()
        # if the link is broken, we remove the client
        remove(socket)

def remove(socketToRemove):
    global clientStates
    global clientConnections
    print("remove()")
    connectionToDelete = None
    stateToDelete = None
    removedID = None

    for key in clientStates:
        clientSocket = clientConnections[key]['socket']
        if(clientSocket == socketToRemove):
            print("disconnecting client: "+str(key)+" on socket: "+str(socketToRemove))
            removedID = key

    if removedID!=None:
        del clientStates[removedID]
        del clientConnections[removedID]

    print("remaning clientStates: "+str(clientStates))
    print("remaning clientConnections: "+str(clientStates))

    print("notifying other clients of client removal")
    quitEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.PLAYER_QUIT,removedID)
    broadcast(quitEvent, None)

while True:

    """Accepts a connection request and stores two parameters,
    conn which is a socket object for that user, and addr
    which contains the IP address of the client that just
    connected"""
    try:
        #print("waiting for new clients...")
        conn, addr = server.accept()
        conn.settimeout(15)
        """Maintains a list of clients for ease of broadcasting
        a message to all available people in the chatroom"""

        # prints the address of the user that just connected
        print(str(addr) + " connected")

        # creates and individual thread for every user
        # that connects
        #start_new_thread(clientThread,(conn,addr))
        threading.Thread(target=clientThread,
            args=(conn,addr)
        ).start()
        print("client thread started")
    except:
        print(traceback.format_exc())

conn.close()
server.close()
