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
    currentScene = logic.getCurrentScene()
    currentScene.replace("UI-graphics")

def radioSetupAction():
    currentScene = logic.getCurrentScene()
    currentScene.replace("UI-settings-radio")
    
def gameOptionsAction():
    currentScene = logic.getCurrentScene()
    currentScene.replace("UI-settings-game")
    
def rateProfileAction():
    currentScene = logic.getCurrentScene()
    currentScene.replace("UI-settings-rates")
    
def backAction():
    bge.logic.sendMessage("cam1")
    currentScene = logic.getCurrentScene()
    sceneHistory = logic.globalDict['sceneHistory']
    print(sceneHistory)
    backScene = sceneHistory[-2]
    removedScene = sceneHistory.pop(-1)
    removedScene = sceneHistory.pop(-1)
    print("removing scene "+str(removedScene))
    currentScene.replace(backScene)

if(owner['init']!=True):
    render.showMouse(1)
    logic.globalDict['sceneHistory'].append(logic.getCurrentScene().name)
    owner['init'] = True
    window = UI.Window()

    inset = 0.2
    
    mainMenuBlock = UI.BoxElement(window,[50,95],11,1, blockColor, 1)
    mainMenuText = UI.TextElement(window,mainMenuBlock.position, textColor, 0, "SETTINGS MENU")

    
    gameOptionsBlock = UI.BoxElement(window,[30,30],2,1, blockColor, 1)
    gameOptionsText = UI.TextElement(window,gameOptionsBlock.position, textColor, 0, "DRONE OPTIONS")
    gameOptionsButton = UI.UIButton(gameOptionsText,gameOptionsBlock,gameOptionsAction)
    
    
    rateOptionsBlock = UI.BoxElement(window,[30,70],2,1, blockColor, 1)
    rateOptionsText = UI.TextElement(window,rateOptionsBlock.position, textColor, 0, "RATE PROFILE")
    rateOptionsButton = UI.UIButton(rateOptionsText,rateOptionsBlock,rateProfileAction)

    
    graphicsBlock = UI.BoxElement(window,[70,70],2,1, blockColor, 1)
    graphicsText = UI.TextElement(window,graphicsBlock.position, textColor, 0, "GRAPHICS")
    graphicsButton = UI.UIButton(graphicsText,graphicsBlock,graphicsAction)

    
    radioSetupBlock = UI.BoxElement(window,[70,30],2,1, blockColor, 1)
    radioSetupText = UI.TextElement(window,radioSetupBlock.position, textColor, 0, "CONTROLLER")
    radioSetupButton = UI.UIButton(radioSetupText,radioSetupBlock,radioSetupAction)

    
    backBlockElement = UI.BoxElement(window,[10,10],1,.5, blockColor, 1)
    backText = UI.TextElement(window,backBlockElement.position, textColor, 0, "BACK")
    backButton = UI.UIButton(backText,backBlockElement,backAction)

else:
    try:
        UI.run(cont)
    except Exception as e:
        utils.log(traceback.format_exc())
        owner['init'] = -1