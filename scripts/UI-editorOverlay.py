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

def updateElementValue(element,value):
    element.setText(value)

if(owner['init']==0):
    owner['init'] = 1
    escToggleHintText = UI.TextElement(window,[10,95], textColor, 0, "esc (toggle menu)",0.75)
    modeHintText = UI.TextElement(window,[7.75,90], textColor, 0, "mode: create",0.75)

    positionBlock = UI.BoxElement(window,[90,97.5],2.75,.5, blockColor, 0.75)
    positionText = UI.TextElement(window,positionBlock.position, textColor, 0, "P 100.0, 100.0, 100.0")

    orientationBlock = UI.BoxElement(window,[62.5,97.5],2.75,.5, blockColor, 0.75)
    orientationText = UI.TextElement(window,orientationBlock.position, textColor, 0, "O 100.0, 100.0, 100.0")

    window.add("positionBlock",positionBlock)
    window.add("positionText",positionText)
    window.add("orientationBlock",orientationBlock)
    window.add("orientationText",orientationText)
    window.add("escToggleHintText",escToggleHintText)
    window.add("modeHintText",modeHintText)

if(owner['init']==1):
    try:
        editor = logic.utils.gameState['mapEditor']
        if(editor != None):
            if(editor.currentMode == editor.MODE_MENU):
                UI.runWindow(window,cont)
                render.showMouse(1)
            else:
                render.showMouse(0)
                digits = 1
                cursorPos = list(logic.utils.gameState['mapEditor'].cursor.position)
                cursorOri = list(logic.utils.gameState['mapEditor'].cursor.orientation.to_euler())
                cursorOri = [math.degrees(cursorOri[0]),math.degrees(cursorOri[1]),math.degrees(cursorOri[2])]
                if(logic.utils.getMapEditor().unitsMetric):
                    unit = 0.1 #metric (the game is scale 10x because of bullet physics)
                    positionValue = "meters: "+str(round(cursorPos[0]*unit,digits))+","+str(round(cursorPos[1]*unit,digits))+","+str(round(cursorPos[2]*unit,digits))
                else:
                    unit = 3.2808*0.1
                    positionValue = "feet: "+str(round(cursorPos[0]*unit,digits))+","+str(round(cursorPos[1]*unit,digits))+","+str(round(cursorPos[2]*unit,digits))
                updateElementValue(window.elements['positionText'], positionValue)

                orientationValue = "degrees: "+str(round(cursorOri[0],digits))+","+str(round(cursorOri[1],digits))+","+str(round(cursorOri[2],digits))
                updateElementValue(window.elements['orientationText'], orientationValue)

                editing = logic.utils.gameState['mapEditor'].editing
                if(editing):
                    mode = "edit"
                else:
                    mode = "create"
                updateElementValue(window.elements['modeHintText'], "mode: "+mode)
        else:

            UI.runWindow(window,cont)
    except Exception as e:
        utils.log(traceback.format_exc())
        owner['init'] = -1
