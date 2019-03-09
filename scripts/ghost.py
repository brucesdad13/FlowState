import bge.logic as logic
owner = logic.getCurrentController().owner
#logic.globalDict['playerQuad'] = owner
utils = logic.utils
def main():
    if(utils.getMode()!=utils.MODE_MULTIPLAYER):
        if('startFinishPlane' in logic.utils.gameState):
            startFinishPlane = logic.utils.gameState['startFinishPlane']
            lap = startFinishPlane['lap']

            if lap < 0:
                logic.ghosts = []
            else:
                if len(logic.ghosts)-1<lap:
                    if(lap<6):
                        ghostObject = addGhostQuad()
                        logic.ghosts.append(createGhostData(owner,ghostObject))
                        print("recording new ghost")
                currentGhost = logic.ghosts[len(logic.ghosts)-1]
                if(lap<6):
                    recordGhostData(owner,currentGhost)
                if len(logic.ghosts)>1:
                    for i in range(0,len(logic.ghosts)-1):
                        lastGhost = logic.ghosts[i]

                        setGhostData(lastGhost)

def createGhostData(obj,ghostObject):
    return {"obj":ghostObject,"currentFrame":0,"frames":[{"pos":list(obj.position),"ori":[list(obj.orientation[0]),list(obj.orientation[1]),list(obj.orientation[2])]}]}

def recordGhostData(obj, currentGhost):
    currentGhost['frames'].append({"pos":list(obj.position),"ori":[list(obj.orientation[0]),list(obj.orientation[1]),list(obj.orientation[2])]})

def setGhostData(ghost):
    frame = ghost["currentFrame"]
    ghost["currentFrame"] += 1
    try:
        ghost['frames'][frame]
    except:
        ghost["currentFrame"] = -1
        frame = 0
    if(ghost['currentFrame'] > 20):
        ghost["obj"].position = ghost["frames"][frame]["pos"]
        ghost["obj"].orientation = ghost["frames"][frame]["ori"]
    else:
        ghost["obj"].position = [0,0,-100000]
def addGhostQuad():
    actuator = owner.actuators["addGhost"]
    actuator.object = "ghostQuad"
    actuator.instantAddObject()
    print(actuator.objectLastCreated)
    obj = actuator.objectLastCreated
    obj.position = [0,0,-100000]
    return obj
main()
