import bge.logic as logic
import math
import random
import os
import copy


cont = logic.getCurrentController()
own = cont.owner
def updateLaps():
    if logic.countingDown:
        own['current_lap'] = 0.00
    logic.currentLap = str(own['lap'])
    logic.lapTimer = own
    if(own['lap'] >0):
        logic.lastLapTime = str(format(own['last_lap'], '.2f'))
        logic.bestLapTime = str(format(own['best_lap'], '.2f')) 
    else:
        logic.lapTimes = []
        logic.currentLap = ""
        logic.lastLapTime = ""
        logic.bestLapTime = ""
    if(own['lap'] == -1):
        logic.holeshotTime = 0.0

    logic.raceTimer = str(format(own['race time'], '.2f'))
    
def addLastLap():
    own['lap']+=1
    #cont.actuators['Sound'].startSound()
    #if(own['lap'] != 0):
    
    if own['lap'] >= 0:
        if own['lap'] > 0:
            own['last_lap'] = copy.deepcopy(own['current_lap'])
        if(logic.finishedLastLap==False):
            logic.lapTimes.append(str(format(own['current_lap'], '.2f')))
            if(logic.lapTimer['race time'] > 120):
                logic.finishedLastLap = True
                logic.utils.gameState['notification']['Text'] = "RACE COMPLETE"
                print("race is complete")
    print("LAPS ARE NOW "+str(own['lap']))
    if(own['lap'] == 0):
        #-logic.utils.gameState['track']['countdownTime']
        logic.holeshotTime = str(format((own['current_lap']), '.2f'))
        print("got holeshot! "+logic.holeshotTime)  
    own['current_lap'] = 0.00
def main():
    collision = cont.sensors['Collision'].triggered and cont.sensors['Collision'].positive
    if(collision):
        if(logic.utils.gameState['track']['nextCheckpoint'] == 1):
            addLastLap()
        
    if(own['last_lap']<own['best_lap']):
        own['best_lap'] = copy.deepcopy(own['last_lap'])
        
    updateLaps() 
if hasattr(logic, 'countingDown'):         
    main()