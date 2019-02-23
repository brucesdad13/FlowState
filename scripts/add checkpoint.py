import bge
logic = bge.logic
render = bge.render
render.showMouse(1)
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
import bge
logic = bge.logic
utils = logic.utils
scene = logic.getCurrentScene()
owner = logic.getCurrentController().owner
parent = owner.parent
checkpoint = scene.addObject(utils.ASSET_CHECKPOINT,owner,0)
checkpoint.setParent(parent)
size = owner.localScale
checkpoint.localScale = [size[0],0.1,size[2]]

utils.addMetadata(checkpoint)
#checkpoint['solid'] = True
owner.endObject()