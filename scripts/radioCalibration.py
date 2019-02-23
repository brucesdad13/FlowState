import bge.logic as logic
import math
import random
import radio as r
cont = logic.getCurrentController()
own = cont.owner
g = logic.globalDict
gravity = 34.0
mass = own.mass

NO_CAL = 0
START_CAL = 1
CALEBRATING = 2
ROLL_SELECT = 3
ROLL_CAL = 4
PITCH_SELECT = 5
PITCH_CAL = 6
YAW_CAL = 7
THROTTLE_SELECT = 8
THROTTLE_CAL = 9
ARM_SELECT = 10
ARM_CAL = 11
RESET_SELECT = 12
RESET_CAL = 13
  
def getHighestDif(channelChanges):
    heighestChannel = 0
    heighestDif = 0
    for channel in channelChanges:
        channelDif = channelChanges[channel]['dif']
        if channelDif > heighestDif:
            print("current channel is "+str(channel))
            print(str(channelDif)+" > "+str(heighestDif))
            heighestChannel = channel
    return heighestChannel


try:
    init = own['init']
    radio = g['radio']
except:
    own['init'] = True
    own['state'] = NO_CAL
    g['radio'] = r.radio(cont.sensors["Joystick"])
    radio = g['radio']
    own['calChannel'] = 0

own['rawInputs'] = radio.getAllRawinputs(cont.sensors["Joystick"])
if own['state'] == START_CAL:
    own['timer'] = 0.00
    own['state'] = ROLL_SELECT
    #initialize
    own['channelChanges'] = {} 
    for i in range(0,len(own['rawInputs'])):
        channelValue = own['rawInputs'][i]
        own['channelChanges'][i] = {'min':own['rawInputs'][i],'max':own['rawInputs'][i], "dif":0}
if own['state'] == ROLL_SELECT:
    if own['timer'] >= 4.00:
        own['state'] = CALEBRATING
        #lets figure out which channel changed the most
        print(own['channelChanges'])
        print(getHighestDif(own['channelChanges']))
    else:
        for i in range(0,len(own['rawInputs'])):
            channelValue = own['rawInputs'][i]
            channelChanges = own['channelChanges'][i]
            if(channelValue > channelChanges['max']):
                channelChanges['max'] = channelValue
            if(channelValue < channelChanges['min']):
                channelChanges['min'] = channelValue
            channelChanges['dif'] = channelChanges['max']-channelChanges['min']


if own['state'] == CALEBRATING:
    own.position = [radio.getRollPercent(),radio.getPitchPercent(),0]