import bge
import math
import traceback
logic = bge.logic
utils = logic.utils
render = bge.render

scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
UI = bge.UI

textColor = [1,1,1,1]
blockColor = [0,0,1,0.75]

if "window" not in owner:
    owner['window'] = UI.Window()
    
window = owner['window']

def playAction():
    mapName = "custom.fmp"
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    render.showMouse(0)
    utils.selectMap(mapName)
    logic.utils.MODE_SINGLE_PLAYER
    currentScene.replace("Main Game")
                
    
def saveAction():
    render.showMouse(0)
    logic.sendMessage("saveMap")
    logic.gameState['mapEditor'].setMode(logic.gameState['mapEditor'].MODE_3D)
    
    
def mainMenuAction():
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    logic.utils.resetGameState()
    logic.utils.MODE_MENU
    currentScene.replace("Menu Background")
    
def helpAction():
    currentScene = logic.getCurrentScene()
    currentScene.replace("UI-editor-help")
    
def inputAction(key,value):
    print("input action")
    print(key)
    print(value)
    #logic.gameState['mapEditor'].selectedAsset['metadata'][key] = value
    logic.gameState['mapEditor'].applyMetadata(key,value)
    
def noAction():
    print("no action")
    
def quitGameAction():
    render.showMouse(0)
    logic.gameState['mapEditor'].setMode(logic.gameState['mapEditor'].MODE_3D)

def resumeAction():
    render.showMouse(0)
    logic.gameState['mapEditor'].setMode(logic.gameState['mapEditor'].MODE_3D)
    
def spawnMetadataInput(window,label,value,position,action,min,max,increment):
    height = position[1]
    width = position[0]
    pos = [62.5,90.5]
    rowBox = UI.BoxElement(window,[50+width,height],4,0.5, blockColor, 5)
    titleText = UI.TextElement(window,[40+width,height], textColor, 0, label)
    
    
    increaseBox = UI.BoxElement(window,[67+width,height],0.5,0.5, blockColor, 1)
    increaseText = UI.TextElement(window,increaseBox.position, textColor, 0, "+")
    increaseButton = UI.UIButton(increaseText,increaseBox,action,label)
    
    
    decreaseBox = UI.BoxElement(window,[55+width,height],0.5,0.5, blockColor, 1)
    decreaseText = UI.TextElement(window, decreaseBox.position, textColor, 0, "-")
    decreaseButton = UI.UIButton(decreaseText,decreaseBox,action,label)
    print(action)
    print("VALUE = "+str(value))
    indicatorText = UI.TextElement(window,[60+width,height], textColor, 0, str(value))
    channelInput = UI.UINumberInput(increaseButton,decreaseButton,indicatorText,value,min,max,increment)
    
    owner['window'].add(label+"RowBox",rowBox)
    owner['window'].add(label+"TitleText",titleText)
    owner['window'].add(label+"IncreaseBox",increaseBox)
    owner['window'].add(label+"IncreaseText",increaseText)
    owner['window'].add(label+"IncreaseButton",increaseButton)
    owner['window'].add(label+"DecreaseBox",decreaseBox)
    owner['window'].add(label+"DecreaseText",decreaseText)
    owner['window'].add(label+"DecreaseButton",decreaseButton)
    owner['window'].add(label+"IndicatorText",indicatorText)
    #owner['window'].add(label+"ChannelInput",channelInput)
    
    return None

if(owner['init']==0):
    render.showMouse(1)
    logic.globalDict['sceneHistory'].append(logic.getCurrentScene().name)
    logic.gameState['lockCursor'] = False
    owner['init'] = 1
    inset = 0.2

    metadataContainerBlock = UI.BoxElement(window,[85,50],5,6, blockColor, -1000)
    
    owner['metadataObject'] = []
    i = 0
    asset = logic.gameState['mapEditor'].selectedAsset
    if(asset!=None):
        if 'metadata' in asset:
            print(asset['metadata'])
        for key in asset['metadata']:
            if(key not in utils.STATIC_METADATA):
                value = asset['metadata'][key]
                metadataInput = spawnMetadataInput(window,key,value,[30,85-(i*10)],inputAction,1,10000,1)
                i+=1
    
    mainMenuBlock = UI.BoxElement(window,[7.5,2.5],1.5,.5, blockColor, 1)
    mainMenuText = UI.TextElement(window,mainMenuBlock.position, textColor, 0, "MAIN MENU")
    mainMenuButton = UI.UIButton(mainMenuText,mainMenuBlock,mainMenuAction)
    
    #playBlock = UI.BoxElement(window,[65,2.5],1,.5, blockColor, 1)
    #playText = UI.TextElement(window,playBlock.position, textColor, 0, "PLAY")
    #playButton = UI.UIButton(playText,playBlock,playAction)
    
    saveBlock = UI.BoxElement(window,[75,2.5],1,.5, blockColor, 1)
    saveText = UI.TextElement(window,saveBlock.position, textColor, 0, "SAVE")
    saveButton = UI.UIButton(saveText,saveBlock,saveAction)

    helpBlockElement = UI.BoxElement(window,[85,2.5],1,.5, blockColor, 1)
    helpText = UI.TextElement(window,helpBlockElement.position, textColor, 0, "HELP")
    helpButton = UI.UIButton(helpText,helpBlockElement,helpAction)

    
    quitBlockElement = UI.BoxElement(window,[95,2.5],1,.5, blockColor, 1)
    quitText = UI.TextElement(window,quitBlockElement.position, textColor, 0, "RESUME")
    quitButton = UI.UIButton(quitText,quitBlockElement,quitGameAction)
    
    
    owner['window'].add("metadataContainerBlock",metadataContainerBlock)
    owner['window'].add("mainMenuBlock",mainMenuBlock)
    owner['window'].add("mainMenuText",mainMenuText)
    owner['window'].add("mainMenuButton",mainMenuButton)
    #owner['window'].add("playBlock",playBlock)
    #owner['window'].add("playText",playText)
    #owner['window'].add("playButton",playButton)
    owner['window'].add("saveBlock",saveBlock)
    owner['window'].add("saveText",saveText)
    owner['window'].add("saveButton",saveButton)
    owner['window'].add("helpBlockElement",helpBlockElement)
    owner['window'].add("helpText",helpText)
    owner['window'].add("helpButton",helpButton)
    owner['window'].add("quitBlockElement",quitBlockElement)
    owner['window'].add("quitText",quitText)
    owner['window'].add("quitButton",quitButton)

if(owner['init']==1):
    try:
        editor = logic.gameState['mapEditor']
        if(editor != None):
            if(editor.currentMode == editor.MODE_MENU):
                UI.runWindow(window,cont)
                
        else:
            
            UI.runWindow(window,cont)
    except Exception as e:
        utils.log(traceback.format_exc())
        owner['init'] = -1
        