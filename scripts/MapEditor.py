import bge
import math
import copy
import time
render = bge.render
logic = bge.logic
utils = logic.utils
#print(logic.getAverageFrameRate())
if(logic.getAverageFrameRate() != 0.0):
    frameTime = 6.0/logic.getAverageFrameRate()
#    print("not one")
else:
    frameTime = 1
def roundTo(x, base):
    return int(base * round(float(x)/base))

class MapEditor:
    MODE_3D = 0
    MODE_MENU = 1
    def __init__(self):
        self.cont = logic.getCurrentController()
        self.owner = self.cont.owner

        self.cursor = self.findChildWithProperty("mapEditorCursor")
        self.camera = self.findChildWithProperty("mapEditorCamera")
        self.cursorOffsetPosition = [0,50,0]
        self.cursorOffsetOrientation = [0,0,0]
        self.cursorOffsetScale = [1,1,1]
        self.lookVelocity = [0,0]
        self.linearVelocity = [0,0]
        self.lookDamp = 0.99
        self.movementDamp = 0.99
        self.fastSpeed = 50
        self.mediumSpeed = 7.5
        self.slowSpeed = 0.08
        self.defaultSensitivity = 0.05
        self.currentSensitivity = 0
        self.posSnap = 10
        self.snapOri = 15
        self.snapScale = 0.1
        self.snapToGround = True
        self.scaleMode = False
        self.altMode = False
        self.moveSpeed = self.mediumSpeed
        self.editing = False

        self.snapOrientation = True
        self.snapPosition = True

        self.cursor.removeParent()
        self.leftClick = self.cont.sensors['MouseLeftButton']
        self.rightClick = self.cont.sensors['MouseRightButton']
        self.scrollUp = self.cont.sensors['MouseWheelUp']
        self.middleClick = self.cont.sensors['MouseMiddle']
        self.scrollDown = self.cont.sensors['MouseWheelDown']
        self.mouseMovement = self.cont.sensors['MouseMovement']

        self.keyboard = self.cont.sensors['Keyboard']

        self.cameraRay = self.cont.sensors['CameraRay']

        self.assetIndex = 0
        self.availableAssets = utils.ASSETS#["asset MGP gate","asset MGP gate large","asset MGP gate hanging large","asset MGP gate high large","asset MGP gate double large","asset MGP ladder large","asset MGP gate angled dive large","asset MGP gate dive large","asset MGP hurdle","asset MGP hurdle large","asset MGP flag","asset pole","asset lumenier gate large","asset table","asset launch pad","asset cone","asset checkpoint square","asset start finish"]
        self.nextAsset = self.availableAssets[self.assetIndex]
        self.selectedAsset = None
        self.addNextAsset()#logic.getCurrentScene().addObject(self.nextAsset,self.cursor,0)
        self.selectedAsset.setParent(self.cursor)


        self.currentMode = self.MODE_3D
        render.showMouse(0)
        print("HIDE MOUSE")

    def findChildWithProperty(self,property):
        print(self.owner.children)
        foundObject = False
        for child in self.owner.children:
            if property in child:
                foundObject = True
                break
        if foundObject == False:
            child = None
        return child

    def updateCursor(self):
        height = 0
        if(self.selectedAsset != None):
            if("assetHeight" in self.selectedAsset):
                height = self.selectedAsset["assetHeight"]
        self.cursor.orientation = self.camera.orientation
        self.cursor.applyRotation([-math.pi/2,0,0],True) #camera has weird axis
        self.cursor.position = self.camera.position
        self.cursor.applyMovement(self.cursorOffsetPosition,True)

        if(self.snapPosition):
            cPos = self.cursor.position
            self.cursor.position = [roundTo(cPos[0],self.posSnap),roundTo(cPos[1],self.posSnap),roundTo(cPos[2],self.posSnap)]
        self.cursor.applyMovement([0,0,height],False)
        self.cursor.orientation = [0,0,0]
        if(self.snapOrientation):
            cOri = self.cursorOffsetOrientation
            self.cursor.applyRotation([math.radians(roundTo(cOri[0],self.snapOri)),math.radians(roundTo(cOri[1],self.snapOri)),math.radians(roundTo(cOri[2],self.snapOri))],True)
        else:
            self.cursor.applyRotation(self.cursorOffsetOrientation,True)

        if(self.snapPosition):
            scale = self.cursorOffsetScale
            self.cursor.localScale = [roundTo(scale[0],self.snapScale),roundTo(scale[1],self.snapScale),roundTo(scale[2],self.snapScale)]
        else:
            self.cursor.localScale = self.cursorOffsetScale


    def placeCurrentAsset(self):
        print("placeCurrentAsset")
        print(self.editing)

        for child in self.selectedAsset.childrenRecursive:
            if("asset" in self.selectedAsset):
                child['spawn'] = True

        self.selectedAsset.removeParent()
        self.makeSolid(self.selectedAsset)
        print("made "+str(self.selectedAsset.name)+" solid")
        print(self.selectedAsset.getPropertyNames())
        if not self.editing:
            self.addNextAsset()
        else:
            self.selectedAsset = None

    def replaceCurrentAsset(self):
        print("replaceCurrentAsset")
        print(self.editing)
        self.selectedAsset.endObject()
        self.nextAsset = self.availableAssets[self.assetIndex]
        self.addNextAsset()

    def addNextAsset(self):
        print("addNextAsset")
        print(self.editing)
        lastAdded = logic.getCurrentScene().addObject(self.nextAsset,self.cursor,0)
        utils.addMetadata(lastAdded)
        self.selectedAsset = lastAdded
        lastAdded.setParent(self.cursor)
        for child in lastAdded.childrenRecursive:
            if 'spawn' in child:
                child['spawn'] = True
        self.makeGhost(self.selectedAsset)


    def deleteCurrentAsset(self):
        if self.selectedAsset != None:
            self.selectedAsset.endObject()
            self.selectedAsset = None

    def deleteAsset(self):
        ray = self.getCameraRay()
        obj = ray[0]
        if(obj!=None):
            if("asset" in obj and "solid" in obj):
                obj.endObject()
        #return rayHit

    def setMode(self,mode):
        self.currentMode = mode
        if mode == self.MODE_MENU:
            render.showMouse(1)
            self.addMenuScene()
        if mode == self.MODE_3D:
            self.centerMouse()
            render.showMouse(0)
            self.removeMenuScene()

    def addMenuScene(self):
        menuScene = "UI-editor-menu"
        logic.addScene(menuScene)

    def removeMenuScene(self):
        menuScene = "UI-editor-menu"
        scenes = logic.getSceneList()
        for scene in scenes:
            if(str(scene)==menuScene):
                scene.end()

    def pushCursor(self):
        ray = self.getCameraRay()
        rayPos = ray[1]
        rayNormal = ray[2]
        if(rayPos!=None):
            distance = self.camera.getDistanceTo(rayPos)
            self.cursorOffsetPosition = [0,distance,0]

    def getKeyStates(self,keyboard):
        pressedKeys = []
        activeKeys = []
        inactiveKeys = []
        releasedKeys = []
        for event in keyboard.events:
            if(event[1] == bge.logic.KX_SENSOR_JUST_ACTIVATED):
                pressedKeys.append(event[0])
            if(event[1] == bge.logic.KX_SENSOR_ACTIVE):
                activeKeys.append(event[0])
            if(event[1] == bge.logic.KX_SENSOR_INACTIVE ):
                inactiveKeys.append(event[0])
            if(event[1] == bge.logic.KX_SENSOR_JUST_DEACTIVATED ):
                releasedKeys.append(event[0])
        return (pressedKeys,activeKeys,inactiveKeys,releasedKeys)

    def handleNewEditState(self):
        if(self.editing):
            self.deleteCurrentAsset()
        else:
            if(self.selectedAsset==None):
                self.addNextAsset()

    def applyMetadata(self,key,value):
        print("applying metadata "+str(key)+": "+str(value)+" to "+str(self.selectedAsset))
        ray = self.getCameraRay()
        if(ray[0]!=None):
            ray[0]['metadata'][key] = copy.deepcopy(value)
            print(self.selectedAsset['metadata'])

    def makeGhost(self, asset):
        try:
            del asset['solid']
        except:
            pass
        for child in asset.childrenRecursive:
            try:
                child.collisionGroup = 2
                del child['solid']
            except:
                pass
        asset.collisionGroup = 2

    def makeSolid(self, asset):
        try:
            asset['solid'] = True
        except:
            pass
        for child in asset.childrenRecursive:
            try:
                child.collisionGroup = 1
                child['solid'] = True
            except:
                pass
        asset.collisionGroup = 1

    def selectAsset(self):
        print("selectAsset")
        print(self.editing)
        ray = self.getCameraRay()
        print(ray)
        if(self.selectedAsset==None):
            if ray[0] != None:
                asset = ray[0]
                if 'asset' in asset:

                    if(asset.parent != None):
                        asset.removeParent()
                    self.makeGhost(asset)
                    if 'metadata' not in asset:
                        utils.addMetadata(asset)
                    for child in asset.childrenRecursive:
                        self.makeGhost(child)
                        if 'asset' in child:
                            utils.addMetadata(child)
                        print(child.attrDict)
                    assetOri = copy.deepcopy(asset.worldOrientation)
                    print(assetOri)
                    assetScale = copy.deepcopy(asset.localScale)
                    #self.cursor.localScale = assetScale
                    self.cursorOffsetScale = assetScale
                    aeOri = list(assetOri.to_euler())
                    aeOri = [math.degrees(aeOri[0]),math.degrees(aeOri[1]),math.degrees(aeOri[2])]
                    self.cursorOffsetOrientation = aeOri
                    print(aeOri)
                    self.cursor.worldOrientation = assetOri
                    asset.position = self.cursor.position
                    self.selectedAsset = asset
                    asset.setParent(self.cursor)


    def editAsset(self):
        print("selectAsset")
        print(self.editing)
        ray = self.getCameraRay()
        if ray[0] != None:
            asset = ray[0]
            if 'asset' in asset:
                if asset.name in utils.ASSETS:
                    self.selectedAsset = asset
                    self.enterMenuMode()

    def enter3DMode(self):
        self.centerMouse()
        self.currentSensitivity = 0
        self.setMode(self.MODE_3D)
        if self.editing:
            self.selectedAsset = None

    def enterMenuMode(self):
        self.setMode(self.MODE_MENU)

    def handleInputs(self):
        (pressedKeys,activeKeys,inactiveKeys,releasedKeys) = self.getKeyStates(self.keyboard)

        #mouse controls
        leftClick = self.leftClick.triggered and self.leftClick.positive
        rightClick = self.rightClick.triggered and self.rightClick.positive
        scrollUp = self.scrollUp.triggered and self.scrollUp.positive
        middleClick = self.middleClick.triggered and self.middleClick.positive
        scrollDown = self.scrollDown.triggered and self.scrollDown.positive

        editAddToggle = bge.events.SPACEKEY in pressedKeys
        delete = bge.events.DELKEY in pressedKeys
        backspace = bge.events.BACKSPACEKEY in pressedKeys

        #movement
        forward = bge.events.WKEY in activeKeys
        backward = bge.events.SKEY in activeKeys
        right = bge.events.DKEY in activeKeys
        left = bge.events.AKEY in activeKeys

        snapToggle = bge.events.GKEY in pressedKeys
        toggleScale = bge.events.TKEY in pressedKeys
        resetScaleRot = bge.events.RKEY in pressedKeys

        itemUp = bge.events.UPARROWKEY in pressedKeys
        itemDown = bge.events.DOWNARROWKEY in pressedKeys

        speedUp = bge.events.LEFTSHIFTKEY in activeKeys
        escapeToggle = bge.events.ESCKEY in pressedKeys

        altMode = bge.events.LEFTCTRLKEY in activeKeys
        if self.currentMode == self.MODE_3D:
            if leftClick:
                if self.selectedAsset == None:
                    self.editAsset()
                else:
                    self.placeCurrentAsset()

            if editAddToggle:
                self.editing = not self.editing
                self.handleNewEditState()

            if scrollUp:
                if(self.snapToGround):
                    self.snapToGround = False
                if self.snapPosition:
                    self.cursorOffsetPosition[1]+=5
                else:
                    self.cursorOffsetPosition[1]+=2.5

            if scrollDown:
                if(self.snapToGround):
                    self.snapToGround = False
                if self.snapPosition:
                    self.cursorOffsetPosition[1]-=5
                else:
                    self.cursorOffsetPosition[1]-=2

            if middleClick:
                self.snapToGround = not self.snapToGround

            self.altMode = altMode

            if(self.snapToGround):
                self.pushCursor()

            if(delete) or (backspace):
                self.deleteAsset()

            if snapToggle:
                self.snapPosition = not self.snapPosition

            if toggleScale:
                self.scaleMode = not self.scaleMode
                if(self.scaleMode):
                    self.cursor.replaceMesh("Cursor Scale", 1, 0)
                else:
                    self.cursor.replaceMesh("Cursor Rotate", 1, 0)

            if resetScaleRot:
                if self.scaleMode:
                    self.cursorOffsetScale = [1,1,1]
                    #self.cursor.localScale = [1,1,1]
                else:
                    self.cursorOffsetOrientation = [0,0,0]

            f = [0,0]
            if forward:
                f[1] += self.moveSpeed*frameTime

            if backward:
                f[1] -= self.moveSpeed*frameTime

            if right:
                f[0] += self.moveSpeed*frameTime

            if left:
                f[0] -= self.moveSpeed*frameTime

            d = self.movementDamp*frameTime
            v = self.linearVelocity
            self.linearVelocity = [(v[0]*(1-d))+(f[0]*d),(v[1]*(1-d))+(f[1]*d)]
            self.owner.applyMovement([v[0],v[1],0],True)


            if itemUp:
                if(self.assetIndex<len(self.availableAssets)-1):
                    print(self.assetIndex)
                    self.assetIndex+=1
                    self.replaceCurrentAsset()

            if itemDown:
                if(self.assetIndex>0):
                    self.assetIndex-=1
                    self.replaceCurrentAsset()

            if speedUp:
                self.moveSpeed = self.fastSpeed
            else:
                self.moveSpeed = self.mediumSpeed

            self.handleMouseLook()

        if escapeToggle:
            if(self.currentMode == self.MODE_MENU):
                self.enter3DMode()
            else:
                self.enterMenuMode()

    def centerMouse(self):
        windowSize = [render.getWindowWidth(),render.getWindowHeight()]
        center = [int(windowSize[0]/2),int(windowSize[1]/2)]
        render.setMousePosition(center[0],center[1])
        self.mousePosition = center

    def updateMousePosition(self):
        self.mousePosition = self.mouseMovement.position

    def handleMouseLook(self):
        mousePos = self.mousePosition
        rightClick = self.rightClick.positive
        windowSize = [render.getWindowWidth(),render.getWindowHeight()]
        center = [int(windowSize[0]/2),int(windowSize[1]/2)]
        offset = [(center[0]-mousePos[0]),(center[1]-mousePos[1])]
        if rightClick:
            if self.selectedAsset != None:
                if(self.scaleMode == False):
                    cOri = self.cursorOffsetOrientation
                    xOri = math.radians(offset[1])*self.currentSensitivity*50
                    yOri = math.radians(offset[0])*self.currentSensitivity*50
                    if(self.altMode):
                        self.cursorOffsetOrientation = [cOri[0],cOri[1]+xOri,cOri[2]+yOri]
                    else:
                        self.cursorOffsetOrientation = [cOri[0]+xOri,cOri[1],cOri[2]+yOri]
                    if(xOri!=0):
                        print(offset[1])
                else:
                    scale = self.cursorOffsetScale
                    scaleSpeed = 0.1
                    if(self.altMode):
                        newScale = [abs(scale[0]),abs(scale[1]-(offset[0]*self.currentSensitivity*scaleSpeed)),abs(scale[2]+(offset[1]*self.currentSensitivity*scaleSpeed))]
                    else:
                        newScale = [abs(scale[0]-(offset[0]*self.currentSensitivity*scaleSpeed)),abs(scale[1]),abs(scale[2]+(offset[1]*self.currentSensitivity*scaleSpeed))]
                    minScale = 0.1
                    if newScale[0]<minScale:
                        newScale[0] = minScale
                    if newScale[1]<minScale:
                        newScale[1] = minScale
                    if newScale[2]<minScale:
                        newScale[2] = minScale
                    self.cursorOffsetScale = newScale
            else:

                if(self.rightClick.triggered):
                    self.selectAsset()
        else:
            dampening = self.lookDamp*frameTime
            self.lookVelocity = [(offset[0]*dampening)+(self.lookVelocity[0]*(1-dampening)),(offset[1]*dampening)+(self.lookVelocity[1]*(1-dampening))]
            startOri = self.owner.worldOrientation.to_euler()
            self.owner.worldOrientation = [startOri[0],startOri[1],startOri[2]+(self.lookVelocity[0]*0.001)]
            startOri = self.owner.localOrientation.to_euler()
            self.owner.localOrientation = [startOri[0]+(self.lookVelocity[1]*0.001),startOri[1],startOri[2]]

        self.centerMouse()

        self.currentSensitivity = self.defaultSensitivity

    def getCameraRay(self):
        return [self.cameraRay.hitObject,self.cameraRay.hitPosition,self.cameraRay.hitNormal]

    def drawHitCursor(self):
        rayHit = self.getCameraRay()
        hitPos = rayHit[1]
        hitNorm = rayHit[2]
        #render.drawLine(pos,end,[1,1,1])
        if(rayHit[0]!=None):
            render.drawLine(hitPos,[hitPos[0]+hitNorm[0],hitPos[1]+hitNorm[1],hitPos[2]+hitNorm[2]],[1,0,0])

    def menuExists(self):
        existance = False
        scenes = logic.getSceneList()
        if "UI-pause" in scenes:
            existance = True

        return existance

    def run(self):
#                if(logic.utils.gameState['lockCursor'] == True):
        if(self.mouseMovement.triggered and self.mouseMovement.positive):
            if(self.currentMode==self.MODE_3D):
                self.updateMousePosition()
        self.updateCursor()
        self.handleInputs()
        self.drawHitCursor()
        #self.cursor['position'] = str(self.cursor.position)
#            else:
#                logic.utils.gameState['lockCursor'] = True

#try:
def createMapEditor():
    print("setting up new map editor")
    newMapEditor = MapEditor()
    newMapEditor.centerMouse()
    logic.utils.gameState['mapEditor'] = newMapEditor
    print(logic.utils.gameState['mapEditor'])

if('mapEditor' in logic.utils.gameState):
    if logic.utils.gameState['mapEditor'] != None:
    #try:
        logic.utils.gameState['mapEditor'].run()
    #except Exception as e:
    #    utils.log(e)
        #createMapEditor()
    else:
        createMapEditor()
else:
    createMapEditor()

#except Exception as e:
#    if('mapEditor' in logic.utils.gameState):
#        utils.log(e)
