import bge
import copy
import os
logic = bge.logic
class utils:
    ASSET_MGP_GATE = "asset MGP gate"
    ASSET_MGP_GATE_LARGE = "asset MGP gate large"
    ASSET_MGP_GATE_HANGING_LARGE = "asset MGP gate hanging large"
    ASSET_MGP_GATE_HIGH_LARGE = "asset MGP gate high large"
    ASSET_MGP_GATE_DOUBLE_LARGE = "asset MGP gate double large"
    ASSET_MGP_LADDER_LARGE = "asset MGP ladder large"
    ASSET_MGP_GATE_ANGLED_DIVE_LARGE = "asset MGP gate angled dive large"
    ASSET_MGP_GATE_DIVE_LARGE = "asset MGP gate dive large"
    ASSET_MGP_HURDLE = "asset MGP hurdle"
    ASSET_MGP_HURDLE_LARGE = "asset MGP hurdle large"
    ASSET_MGP_FLAG = "asset MGP flag"
    ASSET_MGP_POLE = "asset pole"
    ASSET_LUMENIER_GATE_LARGE = "asset lumenier gate large"
    ASSET_TABLE = "asset table"
    ASSET_LAUNCH_PAD = "asset launch pad"
    ASSET_CONE = "asset cone"
    ASSET_START_FINISH = "asset start finish"
    ASSET_CHECKPOINT = "asset checkpoint square"
    ASSET_CONCRETE_BLOCK = "asset concrete block"
    ASSETS = [ASSET_MGP_GATE,ASSET_MGP_GATE_LARGE,ASSET_MGP_GATE_HANGING_LARGE,ASSET_MGP_GATE_HIGH_LARGE,ASSET_MGP_GATE_DOUBLE_LARGE,ASSET_MGP_LADDER_LARGE,ASSET_MGP_GATE_ANGLED_DIVE_LARGE,ASSET_MGP_GATE_DIVE_LARGE,ASSET_MGP_HURDLE,ASSET_MGP_HURDLE_LARGE,ASSET_MGP_FLAG,ASSET_MGP_POLE,ASSET_LUMENIER_GATE_LARGE,ASSET_TABLE,ASSET_LAUNCH_PAD,ASSET_CONE,ASSET_CONCRETE_BLOCK,ASSET_START_FINISH,ASSET_CHECKPOINT]
    #METADATA_GATE = {"color":None,"skin":None,"foobar":None}
    METADATA_GATE = {"id":-1}
    STATIC_METADATA = ["id"]
    METADATA_CHECKPOINT = {"id":-1,"checkpoint order":1}

    MODE_MENU = 0
    MODE_EDITOR = 1
    MODE_SINGLE_PLAYER = 2
    MODE_MULTIPLAYER = 3


    def __init__(self):
        self.setDefaults()
        self.log("INIT!")
        self.id = 0

    def log(self,error):
        error = str(error)
        userHome = str(logic.expandPath("//"))#os.path.expanduser('~')
        logFile = "flowstate.log"
        path = os.path.join(userHome,logFile)

        print("LOG: "+error)
        with open(path, 'a+') as saveFile:
            saveFile.write(str(error)+"\n")
            saveFile.close()

    def addMetadata(self,asset):
        asset['metadata'] = {}
        if 'gate' in asset.name:
            asset['metadata'] = copy.deepcopy(utils.METADATA_GATE)

        if 'checkpoint' in asset.name:
            asset['metadata'] = copy.deepcopy(utils.METADATA_CHECKPOINT)
        asset['metadata']['id'] = self.getNewID()

    def getNewID(self):
        self.id+=1
        return self.id

    def setDefaultState(self):
        self.log("setting default game state")
        logic.gameState = copy.deepcopy(logic.defaultGameState)

    def resetGameState(self):
        self.log("resetting game state!!!")
        logic.gameState = copy.deepcopy(logic.defaultGameState)

    def selectMap(self,selectedMap):
        logic.gameState["selectedMap"] = selectedMap

    def getSelectedMap(self):
        return logic.gameState["selectedMap"]

    def setMode(self,newMode):
        logic.gameState['mode'] = newMode

    def getMode(self):
        return logic.gameState['mode']

    def getNetworkClient(self):
        print("getting network client "+str(logic.gameState['networkClient']))
        return logic.gameState['networkClient']

    def setNetworkClient(self,client):
        logic.gameState['networkClient'] = client

    def forceDefaults(self,defaultData):
        self.log("Profile versions do not match! You will need to reconfigure your settings ("+logic.globalDict['version']+": "+defaultData['version']+")")
        logic.globalDict = defaultData
        logic.saveGlobalDict()

    def setDefaults(self):
        version = "1.0"
        defaultData = {}
        self.log("updating save file")
        defaultData['version'] = version
        defaultData['sceneHistory'] = []
        defaultData['graphics'] = {}
        defaultData['options'] = {}
        defaultData['radio'] = {}
        defaultData['currentProfile'] = 0
        defaultData['profiles'] = []

        defaultProfile = {}
        defaultProfile['username'] = "Unkown Pilot"
        defaultProfile['color'] = [255,255,255]
        defaultProfile["droneSettings"] = {'cameraTilt':35,'thrust':4800,'rpm':38600,'weight':500,'yawExpo':0.0,'pitchExpo':0.0,'rollExpo':0.0,'pitchRate':100,'rollRate':100,'yawRate':100,'pitchSuperRate':70,'rollSuperRate':70,'yawSuperRate':70}
        defaultProfile['radioSettings'] = {'throttleInverted':False,'yawInverted':False,'pitchInverted':False,'rollInverted':False,'armInverted':False,'resetInverted':False,'yawChannel':1,'pitchChannel':4,'throttleChannel':2,'rollChannel':3,'resetChannel':6,'armChannel':5,'yawOffset':0,'pitchOffset':0,'rollOffset':0,'minThrottle':-32252,'maxThrottle':32252,'minYaw':-32252,'maxYaw':32252,'minPitch':-32252,'maxPitch':32252,'minRoll':-32252,'maxRoll':32252,'minReset':0,'maxReset':32768,'minArm':0,'maxArm':32768,'armSetpoint':0.25,'resetSetpoint':0.25,'dedicatedThrottleStick':True}
        defaultProfile['graphicsSettings'] = {"shaders":True}

        defaultData['profiles'].append(defaultProfile)

        #logic.maps = {"
        logic.defaultGameState = {"selectedMap":"2018 Regional Final.fmp", "notification":{"Text":""}, "mode":self.MODE_MENU, "track":{"countdownTime":5,"checkpoints":[],"nextCheckpoint":1,"lastCheckpoint":1}, "playerData":{"lap":0,"checkpoint":0},"mapEditor":None,"networkClient":None}
        logic.loadGlobalDict()
        self.log(logic.globalDict)
        if('version' in logic.globalDict):
            if(logic.globalDict['version']!=defaultData['version']):
                self.forceDefaults(defaultData)

        else:
            logic.globalDict['version'] = "0.0.0"
            self.forceDefaults(defaultData)

        #add any values not in the old save file
        for key, value in defaultData.items():
            if(key in logic.globalDict):
                pass
            else:
                self.log("old save file was missing key "+str(key))
                logic.globalDict[key] = value

        #remove any values in the old save file which are no longer needed
        garbageKeys = []
        for key, value in logic.globalDict.items():
            if(key in defaultData):
                pass
            else:
                self.log("old save file contains deprecated key "+str(key))
                garbageKeys.append(key)
        for key in garbageKeys:
            del logic.globalDict[key]
