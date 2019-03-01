import bge
import traceback
import time
logic = bge.logic
render = bge.render

scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
UI = bge.UI
utils = logic.utils
textColor = [1,1,1,1]
blockColor = [0,0,1,0.75]

def restartAction():
    render.showMouse(0)
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    currentMap = logic.utils.gameState["selectedMap"]
    logic.utils.resetGameState()
    logic.utils.gameState["selectedMap"] = currentMap
    currentScene.replace("Main Game")

def mainMenuAction():
    if(logic.utils.getMode()==logic.utils.MODE_MULTIPLAYER):
        utils.getNetworkClient().quit()
    else:
        scenes = logic.getSceneList()
        currentScene = logic.getCurrentScene()
        for scene in scenes:
            if(scene!=currentScene):
                scene.end()
        logic.utils.resetGameState()
        logic.utils.setMode(logic.utils.MODE_MENU)
        currentScene.replace("Menu Background")

def settingsAction():
    currentScene = logic.getCurrentScene()
    currentScene.replace("UI-settings")

def quitGameAction():
    logic.endGame()

def resumeAction():
    render.showMouse(0)
    currentScene = logic.getCurrentScene()
    currentScene.end()

if(owner['init']!=True):
    render.showMouse(1)
    logic.globalDict['sceneHistory'].append(logic.getCurrentScene().name)
    owner['init'] = True
    window = UI.Window()

    inset = 0.2

    mainMenuBlock = UI.BoxElement(window,[50,95],11,1, blockColor, 1)
    mainMenuText = UI.TextElement(window,mainMenuBlock.position, textColor, 0, "PAUSE MENU")

    mainMenuBlock = UI.BoxElement(window,[10,50],2,1, blockColor, 1)
    mainMenuText = UI.TextElement(window,mainMenuBlock.position, textColor, 0, "MAIN MENU")
    mainMenuButton = UI.UIButton(mainMenuText,mainMenuBlock,mainMenuAction)

    restartBlock = UI.BoxElement(window,[50,50],2,1, blockColor, 1)
    restartText = UI.TextElement(window,restartBlock.position, textColor, 0, "RESTART")
    restartButton = UI.UIButton(restartText,restartBlock,restartAction)

    settingsBlockElement = UI.BoxElement(window,[90,50],2,1, blockColor, 1)
    settingsText = UI.TextElement(window,settingsBlockElement.position, textColor, 0, "SETTINGS")
    settingsButton = UI.UIButton(settingsText,settingsBlockElement,settingsAction)

    quitBlockElement = UI.BoxElement(window,[90,10],1,.5, blockColor, 1)
    quitText = UI.TextElement(window,quitBlockElement.position, textColor, 0, "QUIT")
    quitButton = UI.UIButton(quitText,quitBlockElement,quitGameAction)

    resumeElement = UI.BoxElement(window,[10,10],1,.5, blockColor, 1)
    resumeText = UI.TextElement(window,resumeElement.position, textColor, 0, "RESUME")
    resumeButton = UI.UIButton(resumeText,resumeElement,resumeAction)


else:
    try:
        UI.run(cont)
    except Exception as e:
        utils.log(traceback.format_exc())
        owner['init'] = -1
