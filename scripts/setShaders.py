import bge
render = bge.render
logic = bge.logic
owner = logic.getCurrentController().owner
utils = logic.utils
profileIndex = logic.globalDict['currentProfile']
profiles = logic.globalDict['profiles']
owner['shaders'] = profiles[profileIndex]['graphicsSettings']['shaders']
if owner['shaders']:
    owner.lens= 5.823523998260498
else:
    owner.lens = 10