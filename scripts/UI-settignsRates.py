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

profileIndex = logic.globalDict['currentProfile']
profiles = logic.globalDict['profiles']
profile = profiles[profileIndex]
droneSettings = profile['droneSettings']


def soloGameAction():
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    currentScene.replace("main regional finals")
    
def setYawRateAction():
    profileIndex = logic.globalDict['currentProfile']
    profiles = logic.globalDict['profiles']
    logic.globalDict['profiles'][profileIndex]['droneSettings']['yawRate'] = yawRateInput.value

def setRollRateAction():
    profileIndex = logic.globalDict['currentProfile']
    profiles = logic.globalDict['profiles']
    logic.globalDict['profiles'][profileIndex]['droneSettings']['rollRate'] = rollRateInput.value
    
def setPitchRateAction():
    profileIndex = logic.globalDict['currentProfile']
    profiles = logic.globalDict['profiles']
    logic.globalDict['profiles'][profileIndex]['droneSettings']['pitchRate'] = pitchRateInput.value
    
def setYawSuperRateAction():
    profileIndex = logic.globalDict['currentProfile']
    profiles = logic.globalDict['profiles']
    logic.globalDict['profiles'][profileIndex]['droneSettings']['yawSuperRate'] = yawSuperRateInput.value

def setRollSuperRateAction():
    profileIndex = logic.globalDict['currentProfile']
    profiles = logic.globalDict['profiles']
    logic.globalDict['profiles'][profileIndex]['droneSettings']['rollSuperRate'] = rollSuperRateInput.value
    
def setPitchSuperRateAction():
    profileIndex = logic.globalDict['currentProfile']
    profiles = logic.globalDict['profiles']
    logic.globalDict['profiles'][profileIndex]['droneSettings']['pitchSuperRate'] = pitchSuperRateInput.value
    
def applySettings():
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            if(scene.name == "Main Game"):
                currentMap = logic.gameState["selectedMap"]
                logic.utils.resetGameState()
                logic.gameState["selectedMap"] = currentMap
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
    
def spawnRateInput(label,height,channelKey,action,min,max,increment):

    rowBox = UI.BoxElement(window,[50,height],11,0.5, blockColor, 5)
    titleText = UI.TextElement(window,[rowBox.position[0]-35,rowBox.position[1]], textColor, 4, label)
    
    
    increaseBox = UI.BoxElement(window,[57,height],0.5,0.5, blockColor, 1)
    increaseText = UI.TextElement(window,increaseBox.position, textColor, 0, "+")
    increaseButton = UI.UIButton(increaseText,increaseBox,action)
    
    
    decreaseBox = UI.BoxElement(window,[45,height],0.5,0.5, blockColor, 1)
    decreaseText = UI.TextElement(window, decreaseBox.position, textColor, 0, "-")
    decreaseButton = UI.UIButton(decreaseText,decreaseBox,action)
    
    indicatorText = UI.TextElement(window,[50,height], textColor, 0, "0")
    channelInput = UI.UINumberInput(increaseButton,decreaseButton,indicatorText,int(droneSettings[channelKey]),min,max,increment)

    return channelInput

if(owner['init']!=True):
    render.showMouse(1)
    logic.globalDict['sceneHistory'].append(logic.getCurrentScene().name)
    profileIndex = logic.globalDict['currentProfile']
    profiles = logic.globalDict['profiles']
    profile = profiles[profileIndex]
    droneSettings = profile['droneSettings']
    owner['init'] = True
    window = UI.Window()

    inset = 0.2
    
    pageHeaderBlock = UI.BoxElement(window,[50,95],11,1, blockColor, 5)
    pageHeaderText = UI.TextElement(window,pageHeaderBlock.position, textColor, 4, "GAME SETTINGS MENU")

    yawRateInput = spawnRateInput("YAW RATE",80,"yawRate",setYawRateAction,0,200,1)
    pitchRateInput = spawnRateInput("PITCH RATE",70,"pitchRate",setPitchRateAction,0,200,1)
    rollRateInput = spawnRateInput("ROLL RATE",60,"rollRate",setRollRateAction,0,200,1)
    
    yawSuperRateInput = spawnRateInput("YAW SUPER RATE",50,"yawSuperRate",setYawSuperRateAction,0,200,1)
    pitchSuperRateInput = spawnRateInput("PITCH SUPER RATE",40,"pitchSuperRate",setPitchSuperRateAction,0,200,1)
    rollSuperRateInput = spawnRateInput("ROLL SUPER RATE",30,"rollSuperRate",setRollSuperRateAction,0,200,1)
    
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