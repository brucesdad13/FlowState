# Python program to implement client side of chat room.
import socket
import select
import sys
import pickle
import time
import ast
import FSNObjects
import traceback
from uuid import getnode as get_mac

class FSNClient:
    def __init__(self, address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.settimeout(10)
        self.serverIP = address#socket.gethostname()
        self.serverConnected = False
        print(self.serverIP)
        self.serverPort = port#5069
        myIP = socket.gethostname()
        self.networkReady = False
        self.delim = b'\x1E'
        self.buffer = b''
        self.state = FSNObjects.PlayerState(None, None, None, None, None)
        self.messageHandler = None
        self.serverReady = True
        self.readyToQuit = False
        self.clientID = str(time.time())+str(get_mac())
        
    def connect(self):
        if(not self.serverConnected):
            self.server.connect((self.serverIP, self.serverPort))
            self.serverConnected = True
        else:
            print("server is already connected!")

    def recvFrame(self):
        frame = None
        read_sockets,write_socket, error_socket = select.select([self.server],[],[],0.0)
        for socks in read_sockets:
            while True:
                try:
                    newData = socks.recv(1)
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
                except Exception as e:
                    print(traceback.format_exc())
                    print("server unresponsive")
                    self.quit()
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
        
    def quit(self):
        print("quit")
        #quitEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.PLAYER_QUIT,self.clientID)
        #self.sendEvent(quitEvent)
        self.server.close()
        self.serverConnected = False
        
    def isConnected(self):
        return self.serverConnected

    def run(self):
        if(self.isConnected()): #the socket is still connected
            if(self.serverReady): #we have recieved an ack since our last message
                messageOut = str(self.state).encode("utf-8")
                self.sendFrame(messageOut)
                self.serverReady = False #this gets set true once we get another ack
            frame = self.recvFrame() #let's recv and handle anything the server has sent
            
                
        

    
    
    
