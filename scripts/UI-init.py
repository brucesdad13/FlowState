import bge
import traceback
logic = bge.logic
render = bge.render
render.showMouse(1)
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
#utils = logic.utils
UI = bge.UI
render.setFullScreen(True)

textColor = [1,1,1,1]
blockColor = [0,0,1,0.75]

def soloGameAction():
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    currentScene.replace("main regional finals")

def multiplayerAction():
    pass

def settingsAction():
    currentScene = logic.getCurrentScene()
    currentScene.replace("UI-settings")



def quitGameAction():
    logic.endGame()



if(owner['init']!=True):
    owner['init'] = True
    window = UI.Window()

    inset = 0.2

    multiplayerGameText = UI.TextElement(window,[10+inset,10], textColor, 0, "Loading...")
else:
    UI.run(cont)
    try:
        UI.run(cont)
    except Exception as e:
        logic.utils.log(traceback.format_exc())
        owner['init'] = -1
