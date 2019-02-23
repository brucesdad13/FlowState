import bge
logic = bge.logic
cont = logic.getCurrentController()
owner = cont.owner
parent = owner.parent
owner['Text'] = parent['Text']