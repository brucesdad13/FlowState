from bge import logic, types, constraints

def SoftBodyPin(softbodyobj, controls):

    """
    Pins the soft body object to an object using its vertices (a control object). It will pin the soft-body
    object to all of the vertices of all of the objects in the controls list. So, for controls pass a list like:
    
    [ControlObject, ControlObject2, etc.]
    
    where ControlObject are Game Objects fetched through the scene list, for example.
    """
    
    softid = softbodyobj.getPhysicsId()
    ctype = 2 # Constraint type, 1 = edge; 0 = point, 2 = angular?

    for c in controls:
    
        cid = c.getPhysicsId()
    
        for vert in range(c.meshes[0].getVertexArrayLength(0)):
        
            vpos = c.meshes[0].getVertex(0, vert).getXYZ()
            
            constraints.createConstraint(softid, cid, ctype, vpos[0], vpos[1], vpos[2], 8, -1, 0.5)

owner = logic.getCurrentController().owner
controls = [owner.children[0]]
SoftBodyPin(owner,controls)