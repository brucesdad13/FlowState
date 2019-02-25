import bge.logic as logic
cont = logic.getCurrentController()
own = cont.owner
if own['lap'] >= 0:
    if(logic.finishedLastLap==False):
        if own.sensors['lap changed'].positive:
            logic.lapTimes.append(str(format(own['current_lap'], '.2f')))
            if(logic.lapTimer['race time'] > 120):
                logic.finishedLastLap = True
                logic.utils.gameState['notification']['Text'] = "race complete"
                print("race is complete")
