import bge.logic as logic
import math
import random
import copy
import bge.render as render
import time
import statistics
utils = logic.utils
cont = logic.getCurrentController()
own = cont.owner
g = {}
profileIndex = logic.globalDict['currentProfile']
droneSettings = logic.globalDict['profiles'][profileIndex]['droneSettings']
radioSettings = logic.globalDict['profiles'][profileIndex]['radioSettings']
g = {**droneSettings, **radioSettings} #merge the two dictionaries
scene = logic.getCurrentScene()
mass = own.mass
gravity = 98*mass
camera = scene.objects['cameraMain']

try:
    logic.lastLogicTic
except:
    logic.lastLogicTic = float(time.time())
    print("creating time")
eTime = float(time.time())-logic.lastLogicTic
logic.lastLogicTic = float(time.time())
if(logic.getAverageFrameRate()!=0):
    dm = (60/logic.getAverageFrameRate())
else:
    dm = 1
if(dm>1):
    dm = 1
def getAngularAcceleration():
    av = own.getAngularVelocity(True)
    
    if "init" in own:
        lastAv = own['lastAngularVel']
        own['angularAcc'] = getArrayProduct([av[0]-lastAv[0],av[1]-lastAv[1],av[2]-lastAv[2]])
        own['lastAngularVel'] = own.getAngularVelocity(True)

def initAllThings():
    print(logic.gameState['track']['checkpoints'])
    logic.gameState['track']['nextCheckpoint'] = 1
    for checkpoint in logic.gameState['track']['checkpoints']:
        if checkpoint['metadata']['checkpoint order'] !=1:
            checkpoint.visible = False
        else:
            checkpoint.visible = True
    #logic.setPhysicsTicRate(120)
    #logic.setLogicTicRate(120)
    print("max logic ticks per frame: "+str(logic.getMaxLogicFrame()))
    print("logic ticks per second: "+str(logic.getLogicTicRate()))
    print("max physics ticks per frame: "+str(logic.getMaxPhysicsFrame()))
    #logic.setLogicTicRate(60)
    
    print("physics ticks per second: "+str(logic.getPhysicsTicRate()))
    logic.ghosts = []
    av = own.getAngularVelocity(True)
    own['airSpeedDiff'] = 0
    own['lastAirSpeedDiff'] = 0
    own['lastAngularVel'] = av
    own['angularAcc'] = 0
    own['settled'] = False
    own['settleStartTime'] = time.time()
    own['settleDuration'] = 0
    own['settleFrameRates'] = []
    launchPos = copy.deepcopy(logic.gameState['launchPads'][0].position)
    own['launchPosition'] = [launchPos[0],launchPos[1],launchPos[2]+1]
    own.position = own['launchPosition']
    print("SPAWNING!!!"+str(logic.gameState['launchPads'][0].position))
    own['rxPosition'] = copy.deepcopy(logic.gameState['launchPads'][0].position)
    own['rxPosition'][2]+=100
    own.orientation = logic.gameState['launchPads'][0].orientation
    own['oporational'] = True
    own['vtxOporational'] = True
    own['damage'] = 0
    own.mass = g['weight']/1000
    print("SETTING MASS"+str(own.mass))
    print(own.mass)
    logic.countingDown = True
    logic.countdown = -1
    logic.finishedLastLap = False
    logic.gameState['notification']['Text'] = ""
    #own['rxPosition'] = [-2279.73,-30.8,90]
    
    print("init")
def getArrayProduct(array):
    a = array[0]
    b = array[1]
    c = array[2]
    return math.sqrt((a**2)+(b**2)+(c**2))
  
def getAcc():
    lv = own.getLinearVelocity(True)
    try:
        own['acc'] = abs(own['lastVel']-getArrayProduct(lv))
        own['airSpeedDiff'] = (own['lastAirSpeedDiff']-lv[2])*0.018
        own['lastVel'] = getArrayProduct(lv)
    except Exception as e:
        try:
            own['lastVel'] = getArrayProduct(lv)
            own['acc'] = abs(own['lastVel']-getArrayProduct(lv))
            own['lastAirSpeedDiff'] = lv[2]
        except Exception as e:
            print(e)
  
def getStickPercentage(min,max,value):
    resolution = abs(min)+abs(max)
    percent = abs(((value-min)/resolution))
    (0+(100/2))/100.0
    return percent

def setup(camera,angle):
    if 'setup' not in own:
        initAllThings()
        angle = (angle/180)*math.pi
        camera.applyRotation([angle,0,0],True)
        own['setup'] = True
        own['canReset'] = False
        
    
def getSwitchValue(switchPercent,switchSetpoint):
    #if(switchInverted):
    #    switch = switchPercent>switchSetpoint
    #else:
    #    switch = switchPercent<switchSetpoint
    switch = switchPercent>switchSetpoint
    return switch
def resetGame():
    #act = own.actuators["restart"]
    #act.useRestart = True
    #cont.activate(act)
    #own.position = logic.gameState['spawnPoints'][0]#own['startPosition']
    #print("SPAWNING!!!"+str(logic.gameState['spawnPoints'][0]))
    #own.orientation = own['startOrientation']
    own.setLinearVelocity([0,0,0],True)
    own.setAngularVelocity([0,0,0],True)
    
    own['lastAv'] = [0,0,0]
    if 'lastVel' in own:
        own['lastVel'] = [0,0,0]
    lapTimer = logic.gameState['startFinishPlane']
    lapTimer['lap'] = -1
    lapTimer['race time'] = 0.0
    for ghost in logic.ghosts:
      ghost['obj'].endObject()
    logic.ghosts = []
    own['canReset'] = False
    initAllThings()
    
    
def getRXVector(scale,rxPos):
    vectTo = own.getVectTo(rxPos)
    v = vectTo[1]
    vs = abs(v[0])+abs(v[1])+abs(v[2])
    vect = [(v[0]/vs)*scale,(v[1]/vs)*scale,(v[2]/vs)*scale]
    return vect

def applyVideoStatic():
    
    hitList = []

    lastHitPos = own.position
    for interference in range(1,100):
        hit = own.rayCast(own['rxPosition'], lastHitPos, 0.0, "", 0, 0, 0)
        hitPos = hit[1]
        if(hitPos == None):
            hitList.append(own['rxPosition'])
            break
        else:
            if(own.getDistanceTo(hitPos)<2):
                hitList.append(own['rxPosition'])
                break
            vScale = 2
            rxVect = getRXVector(vScale,own['rxPosition'])
            
            #print(lastHitPos)
            hitPos = [hitPos[0]+rxVect[0],hitPos[1]+rxVect[1],hitPos[2]+rxVect[2]]
            hitList.append(hitPos)
        lastHitPos = hitPos

    #render.drawLine(own.position,list(hitList[0]),[1,1,1])    
    #for i in range(0,len(hitList)-1):
    #    pos1 = list(hitList[i])
    #    pos2 = list(hitList[i+1])
    #    #render.drawLine(pos1,pos2,[1,1,1])
    #    #render.drawLine(pos1,[pos1[0],pos1[1],pos1[2]+10],[1,0,0])    
    #print(interference)
    interference *= .1
    groundBreakup = (12-own.position[2])*0.3
    if(groundBreakup<1):
      groundBreakup = 1    
    if(interference<1):
      interference = 1  

    camera['rfNoise'] = own.getDistanceTo(own['rxPosition'])*.01*groundBreakup*interference+camera['eNoise']

def killVideo():
    camera['rfNoise'] = 100
  
def stickInputToDPS(rcData, superRate=70, rcRate=90, rcExpo=0.0, superExpoActive=True):
    #0.27
    inputValue = rcCommand(rcData, rcRate, rcExpo)
    angleRate = None
    if (superExpoActive):
        rcFactor = abs(inputValue) / (500 * rcRate / 100)
        rcFactor = 1 / (1 - rcFactor * superRate / 100)
        angleRate = rcFactor * 27 * inputValue / 16
    else:
        angleRate = (superRate + 27) * inputValue / 16
    #angleRate = constrain(angleRate, -8190, 8190); // Rate limit protection
    return angleRate/230

def rcCommand(rcData, rcRate, rcExpo):
    midRc = 1500
    tmp = min(abs(rcData - midRc), 500) / 100
    #tmp = abs(rcData)/100
    result = ((2500 + rcExpo * (tmp * tmp - 25)) * tmp * rcRate / 2500)
    if (rcData < midRc):
        result = -result
    return result



def main():
    #Do the things and the stuff
    setup(camera,g['cameraTilt'])
    joy = cont.sensors["Joystick"]
    propRay = cont.sensors["Ray"]
    axis = joy.axisValues
    #print(axis)
    #xbox controllers....
    if(g['dedicatedThrottleStick'] == False):
        axis[g['throttleChannel']] -= (g['maxThrottle']-g['minThrottle'])/2
    if(axis != []): #if a radio is connected
    
        #stick offsets
        own['channel0'] = axis[0]
        own['channel1'] = axis[1]
        own['channel2'] = axis[2]
        own['channel3'] = axis[3]
        axis[g['rollChannel']]+=g['rollOffset']
        axis[g['yawChannel']]+=g['yawOffset']
        axis[g['pitchChannel']]+=g['pitchOffset']

        values = []
        center = 7000
        sensativity = .0008
        for value in axis:
            values.append((value-center)*sensativity)
            
            
        throttleInverted = -(int(g['throttleInverted'])-0.5)*2
        yawInverted = -(int(g['yawInverted'])-0.5)*2
        pitchInverted = -(int(g['pitchInverted'])-0.5)*2
        rollnverted = -(int(g['rollInverted'])-0.5)*2
        armInverted = -(int(g['armInverted'])-0.5)*2
        resetInverted = -(int(g['resetInverted'])-0.5)*2

        throttle = (axis[g['throttleChannel']-1])*throttleInverted
        yaw = axis[g['yawChannel']-1]*yawInverted
        pitch = axis[g['pitchChannel']-1]*pitchInverted
        roll = axis[g['rollChannel']-1]*rollnverted
        armSwitch = axis[g['armChannel']-1]*armInverted
        resetSwitch = axis[g['resetChannel']-1]*resetInverted

        throttlePercent = (getStickPercentage(g['minThrottle'],g['maxThrottle'],throttle))
        yawPercent = getStickPercentage(g['minYaw'],g['maxYaw'],yaw)
        pitchPercent = getStickPercentage(g['minPitch'],g['maxPitch'],pitch)
        rollPercent = getStickPercentage(g['minRoll'],g['maxRoll'],roll)
        armPercent = getStickPercentage(g['minArm'],g['maxArm'],armSwitch)
        resetPercent = getStickPercentage(g['minReset'],g['maxReset'],resetSwitch)
        armed = getSwitchValue(armPercent,g['armSetpoint']) 
        reset = getSwitchValue(resetPercent,g['resetSetpoint'])
        
    else: #if no radio is connected
        throttlePercent = 0
        yawPercent = 0
        pitchPercent = 0
        rollPercent = 0
        armed = False
        reset = False
    rotationActuator = cont.actuators["movement"] 

    #apply rotational force
    PE = g['pitchExpo']
    RE = g['rollExpo']
    YE = g['yawExpo']
    pp = (pitchPercent-.5)*2
    rp = (rollPercent-.5)*2
    yp = (yawPercent-.5)*2
    logic.errorLog = str(axis)
    ps = 1
    rs = 1
    ys = 1
    if(pp<0):
        ps = -1
    if(rp<0):
        rs = -1
    if(yp<0):
        ys = -1

    dps = 0.0174533
    RE = 1
    EXPO = 0
    #pitchForce = -(((abs(pp)*g['pitchRate']*85)**(RE))*ps)/foo
    #roleForce = (((abs(rp)*g['rollRate']*85)**(RE))*rs)/foo
    #yawForce = -(((abs(yp)*g['yawRate']*85)**(RE))*ys)/foo

    #-(abs(pp)*ps*dps*(g['pitchRate']*200))**((1+RE)*.82515)
    #print(abs(rp))
    #print((abs(rp)*rs*dps*(g['roleRate']*200)))
    #ps*pow((abs(pp)*(g['pitchRate']*200)),abs(pp)+2.2)*.434588)
    a = .48
    b = .834
    #pitchForce = -ps*pow((abs(pp)*(g['pitchRate']*200)),(abs(pp)*(PE)*a)+b)*dps
    #roleForce = rs*pow((abs(rp)*(g['rollRate']*200)),(abs(rp)*(RE)*a)+b)*dps
    #yawForce = -ys*pow((abs(yp)*(g['yawRate']*200)),(abs(yp)*(YE)*a)+b)*dps

    pitchForce = -stickInputToDPS((pitchPercent*1000)+1000,g['pitchSuperRate'],g['pitchRate'],g['pitchExpo'],True)
    roleForce = stickInputToDPS((rollPercent*1000)+1000,g['rollSuperRate'],g['rollRate'],g['rollExpo'],True)
    yawForce = -stickInputToDPS((yawPercent*1000)+1000,g['yawSuperRate'],g['yawRate'],g['yawExpo'],True)

    getAngularAcceleration()
    getAcc()
    if (own['oporational'] == True)&armed:
        if own['settled']:
            if(cont.sensors['PropStrike'].positive):
                print("PROP STRIKE!")
                own['damage'] += own['acc']*0.1*throttlePercent
                print(own['damage'])
            if (own['acc'] > 65*2):
                own['oporational'] = False
                own['vtxOporational'] = False
                #pass
                print("Linear acceleration limit reached")
            if (abs(own['angularAcc']) > 50):
                own['oporational'] = False
                own['vtxOporational'] = False
                #pass
                print("Rotational acceleration limit reached")
            #if (own['acc'] > 35):
            #    if(own['propContact']):
            #        own['damage'] += own['acc']*0.005
            #if (abs(own['angularAcc']) > 25):
            #    if(own['propContact']):
            #        own['damage'] += own['angularAcc']*0.01
            if (own['damage'] > 2.5):
                own['oporational'] = False
                #pass
    lv = own.getLinearVelocity(True)
    if(own['oporational']):
        applyVideoStatic()
        if(armed):
            try:
                if own['airSpeedDiff'] < 0:
                    own['airSpeedDiff'] = 0
                propwash = math.pow((((own['airSpeedDiff']*.3)+(((own['damage']-1)*.5))*2)*.1145),1.5)*((throttlePercent*10)+.4)
                if propwash > 0.08:
                  propwash = 0.08
            except:
                propwash = 0
                
            
            

            #print(thrust)
            lvl = own.localLinearVelocity

            av = own.getAngularVelocity(True)
            
            #if(propRay.positive==False):
            if(not own['propContact']):
                rx = (random.randrange(0,200)-100)/300
                ry = (random.randrange(0,200)-100)/300
                rz = (random.randrange(0,200)-100)/300
                pwrx = (rx*propwash/(1+propwash*1.00005))*88
                pwry = (ry*propwash/(1+propwash*1.00005))*88
                pwrz = (rz*propwash/(1+propwash*1.00005))*88
                
                angularAcc = own['angularAcc']

                #AIR DAMPENING
                #FD = .99978 #use for X
                #FD = .99996 #use for true Z
                fdm = 0.9 #frontalDampeningMultiplier
                qd = [0.013014*dm,0.0111121*dm*fdm,0.0071081*dm*fdm] #air drag
                own.setLinearVelocity([lv[0]/(1+qd[0]),lv[1]/(1+qd[1]),lv[2]/(1+qd[2])],True)

                st = 0.78*dm #how quick can the motor/pid orient the quad
                lav = own.getAngularVelocity(True)
                
                own.setAngularVelocity([((pitchForce+pwrx)*st)+(lav[0]*(1-st)),((roleForce+pwry)*st)+(lav[1]*(1-st)),yawForce+pwrz], True)
                if own.position[2] <0:
                    p = own.position
                    own.position = [p[0],p[1],0]
                    #if av [2] <0:
                        #own.setAngularVelocity([av[0],av[1],0],False)
                #thrust = thrust/((propwash*0.89)+1)
                maxRPM = g['rpm']#29.7230769
                maxThrust = g['thrust']/10
                propLoad = ((((lvl[0]*.1)+(lvl[1]*.1)+(lvl[2]*.8))*3500)/(maxRPM))
                propThrottleCurve = 1.2
                #thrust = ((throttlePercent**propThrottleCurve)*.85)*(maxThrust-((propLoad**propThrottleCurve)/((maxSpeed**propThrottleCurve)/maxThrust)))
                staticThrust = (throttlePercent**propThrottleCurve)*maxThrust*.55#*100)-(currentSpeed/maxSpeed)
                #y = (((1**1.25)*4800)*.75)-x
                thrust = staticThrust-(propLoad)-(propwash*100)
                print(propLoad)
                propPitch = 4.6
                propSize = 5
                newtonToKg = 0.101971621
                motorNumber = 4
                currentRPM = throttlePercent*g['rpm']
                #thrust = 100*((4.392399*(10**-8))*currentRPM*((propSize**3.5)/math.sqrt(propPitch))*((4.23333*(10**-4))*currentRPM*propPitch-(currentSpeed/10)))*newtonToKg*motorNumber
                
                if(thrust<0):
                    thrust = 0
                if 'lastThrust' in own:
                    thrust = (thrust*st)+(own['lastThrust']*(1-st))
                own['lastThrust'] = thrust
                
                if(float(logic.raceTimer)!=0.0):
                    
                    own.applyForce([0,0,thrust],True)
                    

    else:
        thrust = 0
    if(not own['vtxOporational']):
        killVideo()

    if(reset == False)&(own['canReset']==False):
        own['canReset'] = True
    if((reset)&own['canReset']):
        resetGame()
    own['lastAv'] = own.getAngularVelocity(True)
    #if(logic.getAverageFrameRate()>60):
    #    logic.setTimeScale(1)
own.applyForce([0,0,-98*own.mass],False)
def isSettled():
    if not own['settled']:
        fps = logic.getAverageFrameRate()
        avgFPSList = own['settleFrameRates']
        avgFPSList.append(fps)
        deviation = 100
        if(len(avgFPSList)>1):
            deviation = statistics.stdev(avgFPSList)
        if len(avgFPSList)>100:
            if deviation < 300:
                logic.setTimeScale(1)
                own['settled'] = True
        else:
            logic.setTimeScale(0.01)
            own.setLinearVelocity([0,0,0],True)
            own.position = own['launchPosition']
        if len(avgFPSList)>1000:
            del avgFPSList[0]
            own['settled'] = True
            logic.setTimeScale(1)
            utils.log("WARNING!!!: FPS did not become stable after 2000 frames. Expect physics instability...")
            utils.log("standard deviation: "+str(deviation))
    else:
        if(logic.finishedLastLap):
            logic.setTimeScale(0.001)
            #own.setLinearVelocity([0,0,0],True)
        
if(own.sensors['clock'].positive):
    main()
isSettled() 
