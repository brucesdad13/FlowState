# Python program to implement client side of chat room.
import socket
import select
import sys
import pickle
import time
import ast

class FSNClient:
    def __init__(self, name, age):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverIP = socket.gethostname()
        print(serverIP)
        self.serverPort = 5069
        myIP = socket.gethostname()
        self.networkReady = False
        self.delim = b'\x1E'
        self.buffer = b''
        
    def connect(self):
        server.connect((self.serverIP, self.serverPort))

    def recvFrame(self):
        frame = None
        read_sockets,write_socket, error_socket = select.select([self.server],[],[],0.0)
        for socks in read_sockets:
            while True:
                newData = socks.recv(1024)
                self.buffer+=newData
                if delim in self.buffer:
                    delimIndex = self.buffer.find(delim)
                    frame = self.buffer[:delimIndex]
                    frame = ast.literal_eval(frame.decode("utf-8"))
                    print("got message: " + str(frame))
                    self.buffer = self.buffer[delimIndex+1:-1]
                    break
                if len(self.buffer) > 4096:
                    print("message too long! Disregarding")
                    buffer = b''
                    break
                
        return frame

    def sendFrame(self,data):
        data+=delim
        print("sending frame "+str(data))
        server.send(data)

    def run(self):
        t = time.time()    
        out = {"subject":"positionUpdate","time":t}
        messageOut = str(out).encode("utf-8")
        sendFrame(messageOut)
        frame = recvFrame()
        #peerTime = frame['time']

    
    
    
