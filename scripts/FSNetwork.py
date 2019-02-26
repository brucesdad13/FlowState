# Python program to implement client side of chat room.
import FSNClient
import FSNObjects
import socket
import bge
import math
import time
from uuid import getnode as get_mac
import random
logic = bge.logic
scene = logic.getCurrentScene()
playerName = "Sky2"+str(get_mac())
utils = logic.utils
def quitGame():
    print("exiting game")
    try:
        utils.getNetworkClient().quit(playerName)
    except:
        pass
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    utils.resetGameState()
    utils.setMode(utils.MODE_MENU)
    currentScene.replace("Menu Background")
    
def addNewPlayer(playerID):
    print("addNewPlayer("+str(playerID)+")")
    newObj = scene.addObject("playerQuad",logic.player,0)
    logic.peers[playerID] = newObj #lets add this new player model to a dict so we can reference it later
    
def clientMessageHandler(message):
    messageType = message[FSNObjects.MESSAGE_TYPE_KEY]
    #   ("message handler called! "+str(messageType))
    
    #server event
    if messageType == FSNObjects.SERVER_EVENT_TYPE_KEY: 
        #print("handling server event")
        #print("message = "+str(message))
        message = FSNObjects.ServerEvent.getMessage(message)
        if(message.eventType == FSNObjects.ServerEvent.PLAYER_JOINED):
            #print("- player join event")
            addNewPlayer(message.senderID)
        if(message.eventType == FSNObjects.ServerEvent.ACK):
            utils.getNetworkClient().serverReady = True
            
    #player state
    if messageType == FSNObjects.PLAYER_STATE: 
        #print("handling player state")
        #print("message = "+str(message))
        message = FSNObjects.PlayerState.getMessage(message)
        if(message.senderID in logic.peers):
            peerObject = logic.peers[message.senderID]
            peerObject.position = message.position
            peerObject.orientation = message.orientation
            
    #player event       
    if messageType == FSNObjects.PLAYER_EVENT: 
        #print("handling player event")
        #print("message = "+str(message))
        message = FSNObjects.PlayerEvent.getMessage(message)
        if(message.eventType == FSNObjects.PlayerEvent.PLAYER_JOINED):
            #print("- player join event")
            addNewPlayer(message.senderID)
            
    #server state        
    if messageType == FSNObjects.SERVER_STATE: 
        #print("handling server state")
        #print("message = "+str(message))
        message = FSNObjects.ServerState.getMessage(message)
        peerStates = message.playerStates
        for key in peerStates:
            if(key==playerName):
                pass
            else:
                #print(str(key)+" != "+str(playerName))
                peerState = peerStates[key]
                #print(peerStates)
                message = FSNObjects.PlayerState.getMessage(peerState)
                newObj = scene.addObject("playerQuad",logic.player,0)
                print("ADDING NEW PLAYER OBJECT!!!!!")
                logic.peers[key] = newObj #lets add this new player model to a dict so we can reference it later
                #print(logic.peers)
                peerObject = logic.peers[key]
                peerObject.position = message.position
                peerObject.orientation = message.orientation

def setup():
    global playerName
    #playerName += str(random.randint(10000,99999))
    print("setup")
    utils.setNetworkClient(FSNClient.FSNClient(utils.getServerIP(),5069))
    utils.getNetworkClient().connect()
    playerJoinEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.PLAYER_JOINED,playerName)
    utils.getNetworkClient().sendEvent(playerJoinEvent)
    utils.getNetworkClient().setMessageHandler(clientMessageHandler)
    logic.peers = {}

def run():
    position = list(logic.player.position)
    o = logic.player.orientation.to_euler()
    orientation = [o[0],o[1],o[2]]
    color = [0,0,1]
    myState = FSNObjects.PlayerState(playerName,None,position,orientation,color)
        
    utils.getNetworkClient().updateState(myState)
    utils.getNetworkClient().run()

def main():
    if hasattr(logic, 'isSettled'):
        try:
            logic.lastNetworkTick
        except:
            logic.lastNetworkTick = 0
        try:
            logic.lastLogicTic
        except:
            logic.lastLogicTic = float(time.time())
        if utils.getNetworkClient()!=None:
            #if(logic.lastNetworkTick>=0.1):
            #if(logic.lastNetworkTick>=0.01):
            if utils.getNetworkClient().isConnected():
                run()
                logic.lastNetworkTick = 0
            else:
                quitGame()
                
        else:
            setup()
            logic.lastNetworkTick = 0
        lastFrameExecution = float(time.time())-logic.lastLogicTic
        logic.lastNetworkTick+=lastFrameExecution
        
main()