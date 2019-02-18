# Python program to implement client side of chat room.
import socket
import select
import sys
import pickle
import time
import ast
import scripts.FSNObjects

class FSNClient:
    def __init__(self, address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverIP = address#socket.gethostname()
        print(self.serverIP)
        self.serverPort = port#5069
        myIP = socket.gethostname()
        self.networkReady = False
        self.delim = b'\x1E'
        self.buffer = b''
        FSNObjects.playerState
        
    def connect(self):
        self.server.connect((self.serverIP, self.serverPort))

    def recvFrame(self):
        frame = None
        read_sockets,write_socket, error_socket = select.select([self.server],[],[],0.0)
        for socks in read_sockets:
            while True:
                newData = socks.recv(1024)
                self.buffer+=newData
                if self.delim in self.buffer:
                    delimIndex = self.buffer.find(self.delim)
                    frame = self.buffer[:delimIndex]
                    frame = ast.literal_eval(frame.decode("utf-8"))
                    print("got message: " + str(frame))
                    self.buffer = self.buffer[delimIndex+1:-1]
                    break
                if len(self.buffer) > 4096:
                    print("message too long! Disregarding")
                    self.buffer = b''
                    break
                
        return frame

    def sendFrame(self,data):
        data+=self.delim
        print("sending frame "+str(data))
        self.server.send(data)

    def run(self):
        t = time.time()    
        out = {"subject":"positionUpdate","time":t}
        messageOut = str(out).encode("utf-8")
        self.sendFrame(messageOut)
        frame = self.recvFrame()
        #peerTime = frame['time']

    
    
    
