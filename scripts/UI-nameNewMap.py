import bge
import traceback
import os
from os.path import isfile, join
logic = bge.logic
utils = logic.utils
render = bge.render
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
UI = bge.UI
textColor = [1,1,1,1]
blockColor = [0,0,1,0.75]
mapButtons = []
render.showMouse(1)


if "window" not in owner:
    owner['window'] = UI.Window()
    
window = owner['window']

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
    mapButton = UI.UIButton(mapButtonText,mapButtonBlock,createMapAction,"map",name)
    mapButtons.append(mapButton)
    
    owner['window'].add("mapButtonBlock"+name,mapButtonBlock)
    owner['window'].add("mapButtonText"+name,mapButtonText)
    owner['window'].add("mapButton"+name,mapButton)
    

if(owner['init']!=True):
    logic.globalDict['sceneHistory'].append(logic.getCurrentScene().name)
    owner['init'] = True
    window = UI.Window()

    inset = 0.2
    
    headerBox = UI.BoxElement(window,[45,95],11,1, blockColor, 1)
    headerText = UI.TextElement(window,headerBox.position, textColor, 0, "SELECT MAP")
    
    #back button
    nameLabelBlockElement = UI.BoxElement(window,[40,50],10,.5, blockColor, 1)
    nameLabelText = UI.TextElement(window,nameLabelBlockElement.position, textColor, 0, "MAP NAME:")
    nameLabelButton = UI.UIButton(nameLabelText,nameLabelBlockElement,backAction)
    textInput = UI.TextInputElement(window,[55,50], textColor, 0, "new map")

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
    #owner['window'].add("textInput",textInput)

else:
    try:
        #UI.run(cont) 
        UI.runWindow(window,cont)
    except Exception as e:
        utils.log(traceback.format_exc())
        owner['init'] = -1
        