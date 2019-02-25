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
radioSettings = profile['radioSettings']
joy = cont.sensors["Joystick"]
axis = joy.axisValues
def setThrottleChannel(key,value):
    print("got final value "+str(int(throttleInput.value)))
    logic.globalDict['profiles'][profileIndex]['radioSettings'][key] = int(value)

def setYawChannel(key,value):
    print("got final value "+str(int(yawInput.value)))
    logic.globalDict['profiles'][profileIndex]['radioSettings'][key] = int(value)

def setPitchChannel(key,value):
    print("got final value "+str(int(pitchInput.value)))
    logic.globalDict['profiles'][profileIndex]['radioSettings'][key] = int(value)

def setRollChannel(key,value):
    print("got final value "+str(int(rollInput.value)))
    logic.globalDict['profiles'][profileIndex]['radioSettings'][key] = int(value)

def setArmChannel(key,value):
    logic.globalDict['profiles'][profileIndex]['radioSettings'][key] = int(value)

def setResetChannel(key,value):
    logic.globalDict['profiles'][profileIndex]['radioSettings'][key] = int(value)

def handleButtonCallback(dictKey,value):
    logic.globalDict['profiles'][profileIndex]['radioSettings'][dictKey] = value

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

def spawnRadioInput(label,height,channelKey,invertedKey,action,min,max,increment):

    rowBox = UI.BoxElement(window,[50,height],11,0.5, blockColor, 5)
    titleText = UI.TextElement(window,[rowBox.position[0]-30,rowBox.position[1]], textColor, 4, label)

    increaseBox = UI.BoxElement(window,[55,height],0.5,0.5, blockColor, 1)
    increaseText = UI.TextElement(window,increaseBox.position, textColor, 0, "+")
    increaseButton = UI.UIButton(increaseText,increaseBox,action,channelKey)

    decreaseBox = UI.BoxElement(window,[45,height],0.5,0.5, blockColor, 1)
    decreaseText = UI.TextElement(window,decreaseBox.position, textColor, 0, "-")
    decreaseButton = UI.UIButton(decreaseText,decreaseBox,action,channelKey)

    invertedBox = UI.BoxElement(window,[86,height],1,0.5, blockColor, 1)
    invertedLabelText = UI.TextElement(window,[invertedBox.position[0],invertedBox.position[1]], textColor, 0, "INVERTED")
    invertedText = UI.TextElement(window,[invertedBox.position[0]+10,invertedBox.position[1]], textColor, 0, "True")
    invertedButton = UI.UIButton(invertedText,invertedBox,handleButtonCallback)

    indicatorText = UI.TextElement(window,[50,height], textColor, 0, "0")
    channelInput = UI.UINumberInput(increaseButton,decreaseButton,indicatorText,int(radioSettings[channelKey]),min,max,increment)
    invertedBooleanButton = UI.UIBooleanInput(invertedButton,invertedText,invertedKey,radioSettings[invertedKey])
    return channelInput,invertedBooleanButton

if(owner['init']!=True):
    render.showMouse(1)
    logic.globalDict['sceneHistory'].append(logic.getCurrentScene().name)
    owner['init'] = True
    window = UI.Window()

    inset = 0.2

    pageHeaderBlock = UI.BoxElement(window,[50,95],11,1, blockColor, 5)
    pageHeaderText = UI.TextElement(window,pageHeaderBlock.position, textColor, 4, "RADIO SETTINGS MENU")
    owner['radioOutput'] = UI.TextElement(window,[12+inset,22], textColor, 4, "No Radio Detected...")

    throttleInput,throttleInverted = spawnRadioInput("THROTTLE CHANNEL NUMBER",80,"throttleChannel","throttleInverted",setThrottleChannel,1,len(axis),1)
    yawInput,yawInvertedInput = spawnRadioInput("YAW CHANNEL NUMBER",70,"yawChannel","yawInverted",setYawChannel,1,len(axis),1)
    pitchInput,pitchInvertedInput = spawnRadioInput("PITCH CHANNEL NUMBER",60,"pitchChannel","pitchInverted",setPitchChannel,1,len(axis),1)
    rollInput,rollInvertedInput = spawnRadioInput("ROLL CHANNEL NUMBER",50,"rollChannel","rollInverted",setRollChannel,1,len(axis),1)
    resetInput,resetnvertedInput = spawnRadioInput("RESET CHANNEL NUMBER",40,"resetChannel","resetInverted",setResetChannel,1,len(axis),1)
    armInput,armInvertedInput = spawnRadioInput("ARM CHANNEL NUMBER",30,"armChannel","armInverted",setArmChannel,1,len(axis),1)

    #radio channel indicators
    leftStickBox = UI.BoxElement(window,[42.5,10],1,1, blockColor, 1)
    rightStickBox = UI.BoxElement(window,[57.5,10],1,1, blockColor, 1)

    titleText = UI.TextElement(window,[leftStickBox.position[0]+1.5,leftStickBox.position[1]+10], textColor, 4, "throttle/yaw")
    leftStick = UI.UIElement(window,"UICircle",leftStickBox.position,textColor,0.1,0.1,0)
    titleText = UI.TextElement(window,[rightStickBox.position[0]+1.5,rightStickBox.position[1]+10], textColor, 4, "pitch/roll")
    rightStick = UI.UIElement(window,"UICircle",rightStickBox.position,textColor,0.1,0.1,0)
    owner['leftStick'] = leftStick
    owner['rightStick'] = rightStick

    #aux switch indicators
    resetBox = UI.BoxElement(window,[30,10],0.5,1, blockColor, 1)
    titleText = UI.TextElement(window,[resetBox.position[0]-5.5,resetBox.position[1]], textColor, 4, "reset",1)
    owner['resetSwitch'] = UI.BoxElement(window,resetBox.position,0.5,0.5, textColor, 1)


    armBox = UI.BoxElement(window,[70,10],0.5,1, blockColor, 1)
    titleText = UI.TextElement(window,[armBox.position[0]+5,armBox.position[1]], textColor, 4, "arm")
    owner['armSwitch'] = UI.BoxElement(window,armBox.position,0.5,0.5, textColor, 1)

    #back button
    backBox = UI.BoxElement(window,[10,10],1,.5, blockColor, 1)
    backText = UI.TextElement(window,backBox.position, textColor, 0, "BACK")
    backButton = UI.UIButton(backText,backBox,backAction)

    #apply button
    applyBox = UI.BoxElement(window,[90,10],1,.5, blockColor, 1)
    applyText = UI.TextElement(window,applyBox.position, textColor, 0, "APPLY")
    applyButton = UI.UIButton(applyText,applyBox,applySettings)

else:
    try:
        throttleChannel = radioSettings['throttleChannel']-1
        yawChannel = radioSettings['yawChannel']-1
        rollChannel = radioSettings['rollChannel']-1
        pitchChannel = radioSettings['pitchChannel']-1
        resetChannel = radioSettings['resetChannel']-1
        armChannel = radioSettings['armChannel']-1

        throttleRes = radioSettings['maxThrottle']-radioSettings['minThrottle']
        yawRes = radioSettings['maxYaw']-radioSettings['minYaw']
        pitchRes = radioSettings['maxPitch']-radioSettings['minPitch']
        rollRes = radioSettings['maxRoll']-radioSettings['minRoll']
        armRes = radioSettings['maxArm']-radioSettings['minArm']
        resetRes = radioSettings['maxReset']-radioSettings['minReset']

        throttleInverted = -(int(radioSettings['throttleInverted'])-0.5)*2
        yawInverted = -(int(radioSettings['yawInverted'])-0.5)*2
        pitchInverted = -(int(radioSettings['pitchInverted'])-0.5)*2
        rollInverted = -(int(radioSettings['rollInverted'])-0.5)*2
        armInverted = -(int(radioSettings['armInverted'])-0.5)*2
        resetInverted = -(int(radioSettings['resetInverted'])-0.5)*2

        if(axis == []):
            axis = None
            owner['radioOutput'].setText("No known radios were detected...")
        else:
            owner['radioOutput'].setText(str(axis))

            leftStick = owner['leftStick']
            lsCenter = leftStick.getRealTranslatedPosition()

            rightStick = owner['rightStick']
            rsCenter = rightStick.getRealTranslatedPosition()

            armSwitch = owner['armSwitch']
            armCenter = armSwitch.getRealTranslatedPosition()

            resetSwitch = owner['resetSwitch']
            resetCenter = resetSwitch.getRealTranslatedPosition()
            leftStick.owner.position = [lsCenter[0]+((axis[yawChannel]/yawRes)*yawInverted),lsCenter[1]+((axis[throttleChannel]/throttleRes)*throttleInverted),leftStick.depth]
            rightStick.owner.position = [rsCenter[0]+((axis[rollChannel]/rollRes)*rollInverted),rsCenter[1]+((axis[pitchChannel]/pitchRes)*pitchInverted),rightStick.depth]
            armSwitch.owner.position = [armCenter[0],armCenter[1]+((axis[armChannel]/armRes)*armInverted)-(0.25*armInverted),armSwitch.depth]
            resetSwitch.owner.position = [resetCenter[0],resetCenter[1]+((axis[resetChannel]/resetRes)*resetInverted)-(0.25*resetInverted),resetSwitch.depth]
    except Exception as e:
        utils.log(traceback.format_exc())
        #print(e)
        #owner['init'] = -1
    UI.run(cont)
