# import bge
import bge

# get controller 
cont = bge.logic.getCurrentController()

# get object that controller is attached to 
obj = cont.owner

# set collision group
#obj.collisionGroup = 2
#delattr(obj,'solid')
del obj['solid']
print('DONE!!!!!!!!!!')