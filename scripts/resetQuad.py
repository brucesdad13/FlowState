import bge.logic as logic
owner = logic.getCurrentController().owner
owner.position = [owner['startx'],owner['starty'],owner['startz']]
owner.orientation = [[1,0,0],[0,1,0],[0,0,1]]
logic.getCurrentScene().objects['race gate']['current_lap'] = 100.00
logic.getCurrentScene().objects['race gate']['lap'] = -1
lap = logic.getCurrentScene().objects['race gate']['lap']

if lap <= 0:
    logic.ghosts = []
else:
    if len(logic.ghosts)<lap:
        print("recording")
        print(len(logic.ghost))
        logic.ghost.append([owner.position,owner.orientation])
    