# Python program to implement client side of chat room.
import socket
import select
import sys
import pickle
import time
import ast
import FSNObjects

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
        self.state = FSNObjects.PlayerState(None, None, None, None, None)
        self.messageHandler = None
        
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
                    try:
                        frame = ast.literal_eval(frame.decode("utf-8"))
                    except:
                        print("got invalid frame! "+str(frame))
                        frame = None
                    if(frame!=None):
                        #print("got message: " + str(frame))
                        if(self.messageHandler!=None):
                            self.messageHandler(frame)
                        self.buffer = self.buffer[delimIndex+1:-1]
                    else:
                        self.buffer = b''
                    break
                    
                if len(self.buffer) > 4096:
                    print("message too long! Disregarding")
                    self.buffer = b''
                    break
                
        return frame

    def sendFrame(self,data):
        data+=self.delim
        #print("sending frame "+str(data))
        self.server.send(data)

    def updateState(self,newState):
        self.state = newState
        
    def sendEvent(self,event):
        self.sendFrame(str(event).encode("utf-8"))

    def setMessageHandler(self,method):
        self.messageHandler = method

    def run(self):
        #t = time.time()    
        #out = {"subject":"positionUpdate","time":t}
        messageOut = str(self.state).encode("utf-8")
        self.sendFrame(messageOut)
        frame = self.recvFrame()
        #peerTime = frame['time']

    
    
    
