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
#utils = logic.utils

def soloGameAction():
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    render.showMouse(0)
    currentScene.replace("UI-map-select")
 
def deleteMe():
    logic.utils.gameState['selectedMap'] = "custom.fmp"
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    render.showMouse(0)
    logic.utils.setMode(logic.utils.MODE_EDITOR)
    currentScene.replace("UI-map-edit-select")
    
def editorAction():
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    render.showMouse(0)
    currentScene.replace("UI-map-edit-select")
    
def settingsAction():
    bge.logic.sendMessage("cam2")
    currentScene = logic.getCurrentScene()
    currentScene.replace("UI-settings") 
    
def quitGameAction():
    logic.endGame()

def passAction():
    pass


if(owner['init']!=True):
    render.showMouse(1)
    logic.globalDict['sceneHistory'].append(logic.getCurrentScene().name)
    owner['init'] = True
    window = UI.Window()

    inset = 0.2
    
    mainMenuBlock = UI.BoxElement(window,[50,95],10,1, blockColor, 1)
    mainMenuText = UI.TextElement(window,mainMenuBlock.position, textColor, 0, "MAIN MENU")

    
    soloGameBlockElement = UI.BoxElement(window,[10,50],2,1, blockColor, 1)
    soloGameText = UI.TextElement(window,soloGameBlockElement.position, textColor, 0, "SINGLE PLAYER")
    soloGameButton = UI.UIButton(soloGameText,soloGameBlockElement,soloGameAction)

    #asdf = UI.BoxElement(window,[50,50],10,9.9, [1,0,0,.5], 1)
    editorBlockElement = UI.BoxElement(window,[50,50],2,1, blockColor, 1)
    editorText = UI.TextElement(window,editorBlockElement.position, textColor, 0, "MAP EDITOR")
    editorGameButton = UI.UIButton(editorText,editorBlockElement,editorAction)

    settingsBlockElement = UI.BoxElement(window,[90,50],2,1, blockColor, 1)
    settingsText = UI.TextElement(window,settingsBlockElement.position, textColor, 0, "SETTINGS")
    
    settingsButton = UI.UIButton(settingsText,settingsBlockElement,settingsAction)

    
    quitBlockElement = UI.BoxElement(window,[90,10],1,.5, blockColor, 1)
    quitText = UI.TextElement(window,quitBlockElement.position, textColor, 0, "QUIT")
    quitButton = UI.UIButton(quitText,quitBlockElement,quitGameAction)

else:
    try:
        UI.run(cont)
    except Exception as e:
        logic.utils.log(traceback.format_exc())
        owner['init'] = -1