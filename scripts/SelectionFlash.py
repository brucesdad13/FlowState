import time
import math
import bge
logic = bge.logic
owner = logic.getCurrentController().owner

def setColor(color):
    for mesh in owner.meshes:
        for material in mesh.materials:
            material.emit = color

def init():
    owner['colors'] = []
    owner['init'] = True
    
def run():
    if owner['selected']:
        speed = 3
        value = (math.sin(time.time()*speed)+1)/2
        color = [0,0,0]
        color[1] = value+.1
        color[2] = value
        setColor(value)
    else:
        setColor(0)
    
def main():
    if 'init' not in owner:
        init()
    else:
        run()

main()