import bge
logic = bge.logic
utils = logic.utils
render = bge.render
cont = logic.getCurrentController()
owner = cont.owner
for actuator in cont.actuators:
    #print(key)
    #actuator = cont.actuators[key]
    utils.log("initializing sound: "+str(actuator))
    actuator.volume = 0
    actuator.startSound()