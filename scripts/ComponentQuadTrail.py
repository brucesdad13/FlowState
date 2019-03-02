import bge
import copy
import time
from collections import OrderedDict

if not hasattr(bge, "__component__"):
    global render
    render = bge.render
    
class QuadTrail(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("Segment Count", 20),
        ("Node Lifetime (ms)", 30.0),
        ("Color (RGBA)",[1.0,1.0,1.0,1.0])
    ])

    def start(self, args):
        self.trail = []
        self.lastUpdateTime = time.time()
        self.color = list(args['Color (RGBA)'])
        self.segments = args['Segment Count']
        self.nodeLifetime = args['Node Lifetime (ms)']
        for i in range(0,self.segments):
            self.trail.append(list(self.object.position))
        

    def update(self):
        
        if time.time()-self.lastUpdateTime>self.nodeLifetime/1000:
            self.lastUpdateTime = time.time()
                
            #make the first value the quad's current position
            self.trail.insert(0, list(self.object.position))
            
            #delete the last node in the trail to keep it finite
            del self.trail[-1]
        
        self.drawTrail()
            
            
    def drawTrail(self):
        #draw trail
        for i in range(0,self.segments-1):
            nextNode = self.trail[i+1]
            currentNode = self.trail[i]
            alpha = (((self.segments-i)*(100.0/self.segments)))/100.0
            render.drawLine(nextNode,currentNode,[self.color[0],self.color[1],self.color[2],self.color[3]*alpha])
        render.drawLine(self.trail[0],self.object.position,self.color)