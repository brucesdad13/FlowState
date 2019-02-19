# Python program to implement client side of chat room.
import FSNClient
import FSNObjects
import socket
import bge
import math
import time

logic = bge.logic
scene = logic.getCurrentScene()
playerName = "Sky"

def clientMessageHandler(message):
    print("message handler called!")
    messageType = message[FSNObjects.MESSAGE_TYPE_KEY]
    if messageType == FSNObjects.SERVER_EVENT_TYPE_KEY: 
        message = FSNObjects.ServerEvent.getMessage(message)
        if(message.eventType == FSNObjects.ServerEvent.PLAYER_JOINED):
            newObj = scene.addObject("playerQuad",logic.player,0)
            print("ADDING NEW PLAYER OBJECT!!!!!")
            logic.peers[message.extra] = newObj #lets add this new player model to a dict so we can reference it later
            
    if messageType == FSNObjects.PLAYER_STATE: 
        message = FSNObjects.PlayerState.getMessage(message)
        print("message = "+str(message))
        peerObject = logic.peers[message.senderID]
        peerObject.position = message.position
        peerObject.orientation = message.orientation

def setup():
    print("setup")
    logic.client = FSNClient.FSNClient(socket.gethostname(),5069)
    logic.client.connect()
    playerJoinEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.PLAYER_JOINED,playerName)
    logic.client.sendEvent(playerJoinEvent)
    logic.client.setMessageHandler(clientMessageHandler)
    logic.peers = {}

def run():
    position = list(logic.player.position)
    o = logic.player.orientation.to_euler()
    orientation = [o[0],o[1],o[2]]
    color = [0,0,1]
    myState = FSNObjects.PlayerState(playerName,None,position,orientation,color)
        
    logic.client.updateState(myState)
    logic.client.run()
    

def main():
    
    if hasattr(logic, 'client'):
        if(logic.lastNetworkTick>=0.05):
            run()
            logic.lastNetworkTick = 0
    else:
        setup()
        logic.lastNetworkTick = 0
    lastFrameExecution = float(time.time())-logic.lastLogicTic
    logic.lastNetworkTick+=lastFrameExecution
main()