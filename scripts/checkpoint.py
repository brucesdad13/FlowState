import time
import bge
logic = bge.logic
utils = logic.utils
#try:
#    currentTime = time.time()
#    print(logic.lastTime-currentTime)
#    logic.lastTime = currentTime
#except:
#    logic.lastTime = currentTime


import numpy as np
import math as m

cont = logic.getCurrentController()
owner = cont.owner

def angle(v1, v2, acute):
    
    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    #if (acute == True):
    #    return angle
    #else:
    #    return 2 * np.pi - angle
    return angle
def setCheckpointVisibilities():
    for checkpoint in logic.utils.gameState['track']['checkpoints']:
        if(checkpoint['metadata']['checkpoint order'] == logic.utils.gameState['track']['nextCheckpoint']):
            #checkpoint.visible = True
            checkpoint.visible = False
        else:
            checkpoint.visible = False
def getNormalVect(vect):
    max = 0
    for i in vect:
        if abs(i) > max:
            max = i
    normal = []
    for i in range(0,len(vect)):
        normal.append(vect[i]/max)
    return normal
entrance = owner.children[0]
o = owner.getVectTo(entrance.position)[1]


colSensor = cont.sensors['Collision']
hitObject = colSensor.hitObject

if colSensor.positive and colSensor.triggered:
    owner['checked'] = True
    if(hitObject!=None):
        
        v = hitObject.getLinearVelocity(False)
        #print("v: "+str(v))
        #print("o: "+str(o))
        nextCheckpoint = logic.utils.gameState['track']['nextCheckpoint']
        hitCheckpointNumber = owner['metadata']['checkpoint order']
        if(nextCheckpoint==hitCheckpointNumber):
            difAngle = m.degrees(angle(v,o,True))
            if(difAngle>90):
                if logic.utils.gameState['track']['lastCheckpoint']==hitCheckpointNumber:
                    logic.utils.gameState['track']['nextCheckpoint'] = 1
                else:
                    logic.utils.gameState['track']['nextCheckpoint']+=1
                setCheckpointVisibilities()
                #soundActuator = cont.actuators['Sound']
                #soundActuator.volume = 1
                #soundActuator.startSound()
                print("CHECKPOINT!")