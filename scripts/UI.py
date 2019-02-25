import bge
from inspect import signature
logic = bge.logic
#utils = logic.utils
render = bge.render
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
TEXT = "UIText"
INPUT = "UIInput"
BOX = "UIBox"
BUTTON = 2
NUMBER_INPUT = 3
STICK_DISPLAY = 4
BOOLEAN_INPUT = 5
LIST = 6
class UI:
    def __init__(self):
        self.cont = controller
        self.owner = controller.owner
        self.owner['lastHitObject'] = None

    def runWindow(window, cont):
        owner = cont.owner
        mouseSensor = cont.sensors['Mouse']
        #THIS IS WHERE YOU LEFT OFF
        wheelUp = cont.sensors['MouseWheelUp']
        wheelDown = cont.sensors['MouseWheelDown']
        hitObject = mouseSensor.hitObject

        inputs = logic.mouse.activeInputs

        for key in window.elements:
            element = window.elements[key]
            if(element.disabled==False):
                #if element.primative:
                if(hitObject == element.owner):
                    if(element.type == BUTTON):
                        if (hitObject!=None):
                            element.highlight()
                            for inputKey in inputs:
                                input = inputs[inputKey]
                                if(input.released):
                                    if(input.type == bge.events.LEFTMOUSE):
                                        #element.owner['action']()
                                        element.performAction()

                else:
                    if(element.type == BUTTON):
                        element.deHighlight()

                if(element.type == LIST):
                    if(wheelDown.positive):
                        element.scrollUp()
                        print("scroll up")
                    if(wheelUp.positive):
                        element.scrollDown()
                        print("scroll down")

    def run(cont): #PLEASE DEPRECATE ME BY ADDING PAGE ELEMENTS TO SCREEN ELEMENTS
        owner = cont.owner
        mouseSensor = cont.sensors['Mouse']
        hitObject = mouseSensor.hitObject

        if("lastHitObject" in owner):
            pass
        else:
            owner['lastHitObject'] = None

        if(hitObject != None):
            if(owner['lastHitObject']!=hitObject):
                if hitObject!=None:
                    if("button" in hitObject.getPropertyNames()):

                        hitObject['button'].highlight()
                        owner['lastHitObject'] = hitObject


        if(hitObject == None)or(owner['lastHitObject']!=hitObject):
            if owner['lastHitObject']!=None:
                if("button" in owner['lastHitObject'].getPropertyNames()):
                    owner['lastHitObject']['button'].deHighlight()
                    owner['lastHitObject'] = None

        inputs = logic.mouse.activeInputs
        for inputKey in inputs:
            input = inputs[inputKey]

            if(input.type == bge.events.LEFTMOUSE):
                if(input.released):
                    if(hitObject != None):
                        element = hitObject['UIElement']
                        if("button" in hitObject.getPropertyNames()):
                            element = element.button
                            if 'value' in hitObject and hitObject['value']!=None:
                                logic.utils.log(hitObject['value'])

                                element.performAction()
                            else:
                                element.performAction()
    class Window:
        def __init__(self):
            self.height = 600#render.getWindowHeight() #A BUG NEEDS TO BE REPORTED FOR LETTERBOX
            self.width = 800#render.getWindowWidth()
            self.ratio = self.width/self.height
            self.elements = {}
            logic.utils.log(str(self.height/self.height)+":"+str(self.width/self.height))

        def add(self,id,element):
            self.elements[id] = element

        #def get(self,id):
        #    element = self.elements[id]
        #    print(element)
        #    return element

    class UIElement:
        primative = True
        def __init__(self,window,type,position,color,width,height,depth=0,parent=[],children=[]):
            self.window = window
            self.owner = None
            self.color = color
            self.type = type
            self.position = position
            self.depth = depth
            self.width = width
            self.height = height
            self.parent = parent
            self.children = children
            self.disabled = False
            self.spawnElement()

        def setColor(self,newColor):
            self.owner.color = newColor
            for mesh in self.owner.meshes:
                for mat in range(0,len(mesh.materials)):
                    vertArray = mesh.getVertexArrayLength(mat)
                    for v in range(0,vertArray):
                        vert = mesh.getVertex(mat,v)
                        vert.color = newColor

        def spawnElement(self):
            self.owner = scene.addObject(self.type)
            self.updateElementPosition()
            self.setScale()
            self.setColor(self.color)
            self.owner['UIElement'] = self

        def disable(self):
            self.owner.visible = True
            self.disabled = True

        def enable(self):
            self.owner.visible = False
            self.disabled = False

        def updateElementPosition(self):

            self.owner.position = self.getRealTranslatedPosition()

        def getRealTranslatedPosition(self):
            if(self.window.ratio > 1):
                #width is larger than height

                offsetX = 5
                offsetY = ((5/self.window.ratio))
                xScale = 0.1
                yScale = 0.1/self.window.ratio

            else:
                offsetX = ((5/self.window.ratio))
                offsetY = 5
                xScale = 0.1/self.window.ratio
                yScale = 0.1
            return [(self.position[0]*xScale)-(offsetX),(self.position[1]*yScale)-(offsetY),-self.depth]
        def setScale(self):
            self.owner.localScale = [self.width,self.height,1]

    class TextElement(UIElement):
        primative = True
        def __init__(self,window,position,color=[255,255,255],depth=0,text="",scale=1,parent=[],children=[]):
            self.window = window
            self.owner = None
            self.type = TEXT
            self.color = color
            self.scale = scale
            self.textHang = -0.8
            self.centerOffset = self.getCenteredTextOffset(text)
            self.position = self.getCenteredTextPosition(position)
            self.depth = depth
            self.width = 0.2
            self.height = 0.2
            self.parent = parent
            self.children = children
            self.text = text
            self.disabled = False
            self.spawnElement()

        def getCenteredTextOffset(self,text):
            return len(text)*0.55*self.scale

        def getCenteredTextPosition(self,position):
            return [position[0]-self.centerOffset,position[1]+self.textHang]

        def enable(self):
            super(UI.TextElement, self).enable()

        def disable(self):
            super(UI.TextElement, self).disable()

        def setText(self,newText):
            self.text = newText
            self.owner.text = self.text
            self.getCenteredTextOffset(self.text)
            self.getCenteredTextPosition(self.position)

        def spawnElement(self):
            super(UI.TextElement, self).spawnElement()
            self.owner.text = self.text
            self.owner.localScale = [self.scale*0.2,self.scale*0.2,self.scale*0.2]

    class TextInputElement(UIElement):
        primative = True
        def __init__(self,window,position,color=[255,255,255],depth=0,text="",scale=1,parent=[],children=[]):
            self.window = window
            self.owner = None
            self.type = INPUT
            self.color = color
            self.scale = scale
            self.textHang = -0.8
            self.centerOffset = self.getCenteredTextOffset(text)
            self.position = self.getCenteredTextPosition(position)
            self.depth = depth
            self.width = 0.2
            self.height = 0.2
            self.parent = parent
            self.children = children
            self.text = text
            self.disabled = False
            self.spawnElement()

        def getCenteredTextOffset(self,text):
            return len(text)*0.55*self.scale

        def getCenteredTextPosition(self,position):
            return [position[0]-self.centerOffset,position[1]+self.textHang]

        def enable(self):
            super(UI.TextElement, self).enable()

        def disable(self):
            super(UI.TextElement, self).disable()

        def setText(self,newText):
            self.text = newText
            #self.owner.text = self.text
            self.getCenteredTextOffset(self.text)
            self.getCenteredTextPosition(self.position)

        def spawnElement(self):
            self.owner = scene.addObject("UIInput")
            self.updateElementPosition()
            self.setScale()
            self.setColor(self.color)
            self.owner['UIElement'] = self

            self.owner.text = self.text
            self.owner.localScale = [self.scale*0.2,self.scale*0.2,self.scale*0.2]

    class BoxElement(UIElement):
        primative = True
        def __init__(self,window,position,width,height,color=[1,1,1,1],depth=0,parent=[],children=[]):
            self.window = window
            self.owner = None
            self.type = BOX
            self.color = color
            self.boxOffset = 0.5
            self.position = position
            self.depth = depth
            self.width = width
            self.height = height
            self.parent = parent
            self.children = children
            self.disabled = False
            self.spawnElement()
        def enable(self):
            super(UI.TextElement, self).enable()

        def disable(self):
            super(UI.TextElement, self).disable()
    class UIStickDisplay:
        primative = False
        def __init__(self,dotElement,boxElement,action):
            self.text = textElement
            self.box = boxElement
            self.type = STICK_DISPLAY
            self.box.owner['highlight'] = self.highlight
            self.box.owner['deHighlight'] = self.deHighlight
            self.box.owner['button'] = False
            self.box.owner['action'] = action
            self.disabled = False

        def performAction(self):
            self.box.owner['action']()

    class UIButton:
        primative = False
        def __init__(self,textElement,boxElement,action,key=None,value=None):
            self.text = textElement
            self.type = BUTTON
            self.box = boxElement
            self.box.button = self
            self.box.owner['button'] = self
            self.owner = self.box.owner
            self.action = action
            self.value = value
            self.key = key
            self.value = value
            self.disabled = False
            self.subscriptions = []

        def subscribe(self,method):
            self.subscriptions.append(method)

        def highlight(self):
            s = 1.1
            scale = [self.box.width,self.box.height,1]
            self.box.owner.localScale = [scale[0]*s,scale[1]*s,1]

        def deHighlight(self):
            self.box.owner.localScale = [self.box.width,self.box.height,1]

        def performAction(self):
            sig = signature(self.action)
            params = sig.parameters
            if len(params) == 0:
                for subscriber in self.subscriptions:
                    subscriber(None,None)
                self.action()
            else:
                for subscriber in self.subscriptions:
                    subscriber(self.key,self.value)
                self.action(self.key,self.value)

        def getAction(self):
            return self.action

    class UIList:
        primative = False
        def __init__(self,boxElement,items,spacing):
            self.items = items
            self.box = boxElement
            self.type = LIST
            self.box.owner['list'] = self
            self.box.list = self
            self.scrollPosition = 0
            self.spacing = spacing
            self.disabled = False
            self.maxScrollPosition = 10
            self.minScrollPosition = 0
            self.owner = None

        def scrollUp(self):
            if(self.scrollPosition<self.maxScrollPosition):
                self.scrollPosition += 1
                for element in self.items:
                    self.moveElements(element,1)
                print(self.scrollPosition)

        def scrollDown(self):
            if(self.scrollPosition>self.minScrollPosition):
                self.scrollPosition -= 1
                for element in self.items:
                    self.moveElements(element,-self.spacing)
                print(self.scrollPosition)

        def moveElements(self,element,distance):
            if element.type == BUTTON:
                textStartPos = element.text.position
                element.text.position = [textStartPos[0],textStartPos[1]+(distance*10)]
                element.text.updateElementPosition()

                boxStartPos = element.box.position
                element.box.position = [boxStartPos[0],boxStartPos[1]+(distance*10)]
                element.box.updateElementPosition()
                print("moving")



    class UINumberInput:
        primative = False
        def __init__(self,increaseButton,decreaseButton,indicatorText,value=0,min=None,max=None,increments=1):
            self.value = value
            self.type = NUMBER_INPUT
            self.min = min
            self.max = max
            self.increments = increments
            self.text = indicatorText
            self.increaseButton = increaseButton
            self.decreaseButton = decreaseButton
            #self.secondaryIncreaseAction = self.increaseButton.getAction()
            #self.secondaryDecreaseAction = self.decreaseButton.getAction()
            #self.increaseButton.setAction(self.increaseAction)
            #self.decreaseButton.setAction(self.decreaseAction)
            self.increaseButton.subscribe(self.increaseAction)
            self.decreaseButton.subscribe(self.decreaseAction)
            self.disabled = False
            self.refreshValue()

        def increaseAction(self,key,value):
            if((self.value + self.increments)<=self.max):
                self.value += self.increments
            else:
                self.value = self.max
            self.refreshValue()
            self.increaseButton.value = self.value
            #self.increaseButton.performAction()
            #self.secondaryIncreaseAction(self.increaseButton.key,self.increaseButton.value)

        def decreaseAction(self,key,value):
            if((self.value - self.increments)>=self.min):
                self.value -= self.increments
            else:
                self.value = self.min
            self.refreshValue()
            self.decreaseButton.value = self.value
            #self.decreaseButton.performAction()

        def refreshValue(self):
            self.text.owner['Text'] = self.value

    class UIBooleanInput:
        primative = False
        def __init__(self,button,indicatorText,key,value=False):
            self.value = value
            self.type = BOOLEAN_INPUT
            self.text = indicatorText
            self.key = key
            self.button = button
            self.secondaryAction = self.button.getAction()
            #self.button.setAction(self.action)
            self.button.subscribe(self.action)
            self.disabled = False
            self.refreshValue()

        def action(self,key,value):
            if(self.value):
                self.value = False
            else:
                self.value = True
            self.refreshValue()
            self.button.value = self.value
            self.button.key = self.key
            #self.secondaryAction(self.dictKey,self.value)

        def refreshValue(self):
            self.text.owner['Text'] = str(self.value)

bge.UI = UI
