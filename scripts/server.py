# Python program to implement server side of chat room.
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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
delim = b'\x1E'
# takes the first argument from command prompt as IP address
IP_address = "0.0.0.0"#socket.gethostname()

# takes second argument from command prompt as port number
port = 5069

serverName = "noobs only"

"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
print("binding to "+str(IP_address)+":"+str(port))
server.bind((IP_address, port))
server.settimeout(30)

"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)

connectionList = []
clientStates = {}
outboundMessages = []

def outboundMessageThread():
    global outboundMessages
    while True:
        socketsToDisconnect = []
        if(len(outboundMessages)>0):
            #print("we've got something to send")
            message = outboundMessages.pop(0)
            socket = message['socket']
            data = message['data']
            try:
                dataOut = str(data).encode("utf-8")+delim
                #print("sending message to client: "+str(socket.getpeername()[0])+": "+str(dataOut))
                socket.send(dataOut)
            except Exception as e:
                print(traceback.format_exc())
                socketsToDisconnect.append(socket)

        for socket in socketsToDisconnect:
            try:
                socket.close()
                # if the link is broken, we remove the client
                connectionList.remove(socket)
            except:
                pass

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
                        event = FSNObjects.ServerState(clientStates)
                        broadcast(event,conn)
                        #a new player is joining the game
                        if(message.eventType==FSNObjects.PlayerEvent.PLAYER_JOINED):
                            #let's let him know the state of the game
                            serverState = FSNObjects.ServerState(clientStates)
                            send(serverState,conn)
                            #let's associate the player state with this socket
                            for clientConnection in connectionList:
                                if(clientConnection['socket'] == conn):
                                    clientConnection['senderID'] = message.senderID
                        if(message.eventType==FSNObjects.PlayerEvent.PLAYER_QUIT):
                            #removeByID(senderID)
                            remove(conn)
                            connectionOpen = False


                    #a player is sending an update about their current state
                    if messageType == FSNObjects.PLAYER_STATE:
                        #print("Got a player state. Updating client states")
                        message = FSNObjects.PlayerState.getMessage(frame)
                        senderID = message.senderID
                        newClientState = frame
                        clientStates[senderID] = newClientState
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
    print("sending ack to "+str(socket.getpeername()[0]))
    ack = FSNObjects.ServerEvent(FSNObjects.ServerEvent.ACK)
    send(ack,socket)

def broadcast(message, socket):
    #print("broadcast()")
    for clientConnection in connectionList:
        clientSocket = clientConnection['socket']
        if clientSocket!=socket:
            send(message,clientSocket)

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
        connectionList.remove(socket)

def remove(connection):
    global connectionList
    global clientStates
    print("remove()")
    connectionToDelete = None
    stateToDelete = None
    for i in range(0,len(connectionList)):
        clientConnection = connectionList[i]
        if connection == clientConnection['socket']:
            if(clientConnection['senderID']!=None):
                clientState = clientStates[clientConnection['senderID']]
                print("removing client state: "+str(clientState))
                stateToDelete = clientConnection['senderID']
                #del clientState
            print("disconnecting socket: "+str(clientConnection))
            connectionToDelete = i
            #del clientConnection
    if connectionToDelete!=None:
        del connectionList[connectionToDelete]
    if stateToDelete!=None:
        del clientStates[stateToDelete]
    print("remaning connectionList: "+str(connectionList))
    print("remaning clientStates: "+str(clientStates))

def removeByID(senderID):
    print("removeByID()")
    connectionToDelete = None
    stateToDelete = None
    for clientConnection in connectionList:
        if senderID == clientConnection['senderID']:
            print("disconnecting client: "+str(senderID))
            connectionToDelete = clientConnection
            break

    connectionList.remove(connectionToDelete)
    del clientStates[senderID]
    print(clientConnections)
    print(connectionList)

while True:

    """Accepts a connection request and stores two parameters,
    conn which is a socket object for that user, and addr
    which contains the IP address of the client that just
    connected"""
    try:
        #print(str(len(connectionList))+" clients connected")
        #print("waiting for new clients...")
        conn, addr = server.accept()
        conn.settimeout(15)
        """Maintains a list of clients for ease of broadcasting
        a message to all available people in the chatroom"""
        connectionList.append({"socket":conn,"senderID":None})

        # prints the address of the user that just connected
        print(str(addr) + " connected")

        # creates and individual thread for every user
        # that connects
        #start_new_thread(clientThread,(conn,addr))
        threading.Thread(target=clientThread,
            args=(conn,addr)
        ).start()
        print("client thread started")
        #start_new_thread(outboundMessageThread,())
    except:
        print(traceback.format_exc())

conn.close()
server.close()
