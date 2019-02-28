import bge
import traceback
import os
from os.path import isfile, join
import numpy
logic = bge.logic
utils = logic.utils
render = bge.render
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
UI = bge.UI
textColor = [1,1,1,1]
blockColor = [0,0,1,0.75]
#mapButtons = []
render.showMouse(1)


keyboard = cont.sensors['Keyboard']
blendPath = logic.expandPath("//")

if "window" not in owner:
    owner['window'] = UI.Window()
    
window = owner['window']

def getKeyStates(keyboard):
    pressedKeys = []
    activeKeys = []
    inactiveKeys = []
    releasedKeys = []
    for event in keyboard.events:
        if(event[1] == bge.logic.KX_SENSOR_JUST_ACTIVATED):
            pressedKeys.append(event[0])
        if(event[1] == bge.logic.KX_SENSOR_ACTIVE):
            activeKeys.append(event[0])
        if(event[1] == bge.logic.KX_SENSOR_INACTIVE ):
            inactiveKeys.append(event[0])
        if(event[1] == bge.logic.KX_SENSOR_JUST_DEACTIVATED ):
            releasedKeys.append(event[0])
    return (pressedKeys,activeKeys,inactiveKeys,releasedKeys)

def loadMultiplayerServer(serverName):
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    render.showMouse(0)
    
    utils.setMode(utils.MODE_MULTIPLAYER)
    utils.selectMap("Rotorcross.fmp")
    currentScene.replace("Main Game")
    utils.setServerIP(serverName)

def mapSelectAction(key,mapName):
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    render.showMouse(0)
    utils.selectMap(mapName)
    utils.setMode(utils.MODE_SINGLE_PLAYER)
    currentScene.replace("Map Editor")
 
def multiplayerAction():
    pass
    
def settingsAction():
    bge.logic.sendMessage("cam2")
    currentScene = logic.getCurrentScene()
    currentScene.replace("UI-settings")
    
def backAction():
    currentScene = logic.getCurrentScene()
    sceneHistory = logic.globalDict['sceneHistory']
    print(sceneHistory)
    backScene = sceneHistory[-2]
    removedScene = sceneHistory.pop(-1)
    removedScene = sceneHistory.pop(-1)
    print("removing scene "+str(removedScene))
    currentScene.replace(backScene)

def passAction():
    pass

def addMapButton(name,spacing):
    buttonIndex = len(mapButtons)
    height = 70-(buttonIndex*spacing)
    print(height)
    mapButtonBlock = UI.BoxElement(window,[50,height],5,0.5, blockColor, 1)
    mapButtonText = UI.TextElement(window,mapButtonBlock.position, textColor, 0,name)
    mapButton = UI.UIButton(mapButtonText,mapButtonBlock,mapSelectAction,"map",name)
    mapButtons.append(mapButton)
    
    owner['window'].add("mapButtonBlock"+name,mapButtonBlock)
    owner['window'].add("mapButtonText"+name,mapButtonText)
    owner['window'].add("mapButton"+name,mapButton)
    
def createMapAction():
    currentScene = logic.getCurrentScene()
    sceneHistory = logic.globalDict['sceneHistory']
    print(sceneHistory)
    backScene = sceneHistory[-2]
    removedScene = sceneHistory.pop(-1)
    removedScene = sceneHistory.pop(-1)
    print("removing scene "+str(removedScene))
    currentScene.replace(backScene)
    
def createMapButton(name,spacing):
    buttonIndex = len(mapButtons)
    height = 70-(buttonIndex*spacing)
    print(height)
    mapButtonBlock = UI.BoxElement(window,[50,height],5,0.5, blockColor, 1)
    mapButtonText = UI.TextElement(window,mapButtonBlock.position, textColor, 0,name)
    #mapButton = UI.UIButton(mapButtonText,mapButtonBlock,createMapAction,"map",name)
    #mapButtons.append(mapButton)
    
    owner['window'].add("mapButtonBlock"+name,mapButtonBlock)
    owner['window'].add("mapButtonText"+name,mapButtonText)
    #owner['window'].add("mapButton"+name,mapButton)
    

if(owner['init']!=True):
    logic.globalDict['sceneHistory'].append(logic.getCurrentScene().name)
    owner['init'] = True
    window = UI.Window()

    inset = 0.2
    
    headerBox = UI.BoxElement(window,[45,95],11,1, blockColor, 1)
    headerText = UI.TextElement(window,headerBox.position, textColor, 0, "SELECT MAP")
    
    #back button
    nameLabelBlockElement = UI.BoxElement(window,[40,50],10,.5, blockColor, 1)
    nameLabelText = UI.TextElement(window,nameLabelBlockElement.position, textColor, 0, "SERVER NAME:")
    nameLabelButton = UI.UIButton(nameLabelText,nameLabelBlockElement,backAction)
    textInput = UI.TextInputElement(window,[60,50], textColor, 0, "server ip address",elementObject="UIInput.001")

    #back button
    backBlockElement = UI.BoxElement(window,[10,10],1,.5, blockColor, 1)
    backText = UI.TextElement(window,backBlockElement.position, textColor, 0, "BACK")
    backButton = UI.UIButton(backText,backBlockElement,backAction)
    
    owner['window'].add("backBlockElement",backBlockElement)
    owner['window'].add("backText",backText)
    owner['window'].add("backButton",backButton)
    owner['window'].add("headerBox",headerBox)
    owner['window'].add("headerText",headerText)
    owner['window'].add("mapName",nameLabelButton)
    owner['window'].add("textInput",textInput)
    #owner['window'].add("textInput",textInput)

else:
    try:
        #UI.run(cont) 
        UI.runWindow(window,cont)
        
        #text box stuff. please move into UI TextInput
        (pressedKeys,activeKeys,inactiveKeys,releasedKeys) = getKeyStates(keyboard)
        enter = bge.events.ENTERKEY in pressedKeys
        if(pressedKeys!=[]):
            if(enter):
                #owner['Text'].replace('\n','')
                #owner['Text'].replace('\t',''
                owner['Text'] = owner['Text'].rstrip()
                serverIP = owner['Text']
                print(serverIP)
                loadMultiplayerServer(serverIP)
            else:
                print(pressedKeys)
                #^text box stuff. please move into UI TextInput^
                owner['window'].elements['textInput'].owner['Text'] = owner['Text']
    except Exception as e:
        utils.log(traceback.format_exc())
        owner['init'] = -1
        