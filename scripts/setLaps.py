import bge.logic as logic
import math
import random
import os
cont = logic.getCurrentController()
own = cont.owner

logic.currentLap = str(own['lap'])
logic.lapTimer = own
if(own['lap'] >0):
    logic.lastLapTime = str(format(own['last_lap'], '.2f'))
    logic.bestLapTime = str(format(own['best_lap'], '.2f'))
    
else:
    logic.lapTimes = []
    logic.lastLapTime = ""
    logic.bestLapTime = ""
logic.raceTimer = str(format(own['race time'], '.2f'))
