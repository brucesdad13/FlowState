# Python program to implement client side of chat room.
import socket
import select
import sys
import pickle
import time
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverIP = socket.gethostname()
print(serverIP)
serverPort = 5068
myIP = socket.gethostname()
networkReady = False
print(networkReady)
def setup():
    server.connect((serverIP, serverPort))

def run():
    global time
    # maintains a list of possible input streams
    sockets_list = [server]
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[],0.0)
    for socks in read_sockets:
        messageIn = socks.recv(2048)
        messageIn = pickle.loads(messageIn)
        time = messageIn['time']
    t = time.time()    
    out = {"subject":"positionUpdate","time":t}
    messageOut = pickle.dumps(out)
    server.send(messageOut)

setup()
run()
