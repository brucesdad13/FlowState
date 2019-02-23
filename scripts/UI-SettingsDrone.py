import bge
import traceback
logic = bge.logic
render = bge.render
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
UI = bge.UI

textColor = [1,1,1,1]
blockColor = [0,0,1,0.75]

def soloGameAction():
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    currentScene.replace("main regional finals")
    
def graphicsAction():
    pass

def setThrustAction():
    profileIndex = logic.globalDict['currentProfile']
    profiles = logic.globalDict['profiles']
    logic.globalDict['profiles'][profileIndex]['droneSettings']['thrust'] = thrustInput.value
    print(logic.globalDict['profiles'][profileIndex]['droneSettings']['thrust'])
    bge.logic.sendMessage("loadNewSettings")

def setWeightAction():
    profileIndex = logic.globalDict['currentProfile']
    profiles = logic.globalDict['profiles']
    logic.globalDict['profiles'][profileIndex]['droneSettings']['weight'] = int(weightInput.value)
    bge.logic.sendMessage("loadNewSettings")
    
def setCameraTiltAction():
    profileIndex = logic.globalDict['currentProfile']
    profiles = logic.globalDict['profiles']
    logic.globalDict['profiles'][profileIndex]['droneSettings']['cameraTilt'] = int(camTiltInput.value)
    bge.logic.sendMessage("loadNewSettings")
    
def setRPMAction():
    profileIndex = logic.globalDict['currentProfile']
    profiles = logic.globalDict['profiles']
    logic.globalDict['profiles'][profileIndex]['droneSettings']['rpm'] = int(rpmInput.value)
    bge.logic.sendMessage("loadNewSettings")
    
def applySettings():
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            if(scene.name == "Main Game"):
                currentMap = logic.utils.gameState["selectedMap"]
                logic.utils.resetGameState()
                logic.utils.gameState["selectedMap"] = currentMap
                scene.restart()
    
    logic.saveGlobalDict()
    
def backAction():
    currentScene = logic.getCurrentScene()
    sceneHistory = logic.globalDict['sceneHistory']
    print(sceneHistory)
    backScene = sceneHistory[-2]
    removedScene = sceneHistory.pop(-1)
    removedScene = sceneHistory.pop(-1)
    print("removing scene "+str(removedScene))
    currentScene.replace(backScene)
    
def spawnSetting(label,height,key,action,min,max,increment):
    itemRow = UI.BoxElement(window,[50,height],11,0.5, blockColor, 5)
    itemText = UI.TextElement(window, [itemRow.position[0]-30,itemRow.position[1]], textColor, 4, label)
    
    itemUpBox = UI.BoxElement(window,[60,height],0.5,0.5, blockColor, 1)
    itemUpText = UI.TextElement(window,itemUpBox.position, textColor, 0, "+")
    itemUpButton = UI.UIButton(itemUpText,itemUpBox,action)
    
    itemDownBox = UI.BoxElement(window,[45,height],0.5,0.5, blockColor, 1)
    itemDownText = UI.TextElement(window,itemDownBox.position, textColor, 0, "-")
    itemDownButton = UI.UIButton(itemDownText,itemDownBox,action)
    
    currentItemText = UI.TextElement(window,[50,height], textColor, 0, "")
    return UI.UINumberInput(itemUpButton,itemDownButton,currentItemText,int(droneSettings[key]),min, max, increment)

if(owner['init']!=True):
    render.showMouse(1)
    logic.globalDict['sceneHistory'].append(logic.getCurrentScene().name)
    profileIndex = logic.globalDict['currentProfile']
    profiles = logic.globalDict['profiles']
    profile = profiles[profileIndex]
    droneSettings = profile['droneSettings']
    owner['init'] = True
    window = UI.Window()

    pageHeaderBlock = UI.BoxElement(window,[50,95],11,1, blockColor, 5)
    pageHeaderText = UI.TextElement(window,pageHeaderBlock.position, textColor, 4, "GAME SETTINGS MENU")

    camTiltInput = spawnSetting("CAMERA TILT (DEGREES)",70,"cameraTilt",setCameraTiltAction,0,90,1)
    thrustInput = spawnSetting("STATIC THRUST (GRAMS)",60,"thrust",setThrustAction,0,10000,50)
    weightInput = spawnSetting("ALL UP WEIGHT (GRAMS)",50,"weight",setWeightAction,1,2000,10)
    rpmInput = spawnSetting("RPM",40,"rpm",setRPMAction,0,50400,200)
    
    #back button
    backBlockElement = UI.BoxElement(window,[10,10],1,.5, blockColor, 1)
    backText = UI.TextElement(window,backBlockElement.position, textColor, 0, "BACK")
    backButton = UI.UIButton(backText,backBlockElement,backAction)
    
    #apply button
    applyBox = UI.BoxElement(window,[90,10],1,.5, blockColor, 1)
    applyText = UI.TextElement(window,applyBox.position, textColor, 0, "APPLY")
    applyButton = UI.UIButton(applyText,applyBox,applySettings)

else:
    try:
        UI.run(cont)
    except Exception as e:
        utils.log(traceback.format_exc())
        owner['init'] = -1