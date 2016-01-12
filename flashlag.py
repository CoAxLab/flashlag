#!/usr/bin/env python2

from psychopy import visual, core, event, gui, data
import numpy as np
import time
from math import sin, cos, radians
from random import shuffle, randint, uniform
import os, csv
import random
import math
import os
import pandas as pd

#Set up Output file for reading and writing
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
expName = 'flashLagPilot'  # from the Builder filename that created this script
expInfo = {u'User': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; # Output summary data and analyzed files
filename = _thisDir + os.sep + 'data/%s_%s' %(expInfo['User'], expName)
outputfn =  _thisDir + os.sep +'data/%s_summary_%s_%s.csv' %(expInfo['User'], expName, expInfo['date'])
data_out = pd.DataFrame(columns=('response','actual','correct'))

#Initalize variables
dotRad = (0.1,0.1)
flashRad = (0.1,0.1)
circleRadius = .15
flashRadius = circleRadius+.1
angle = 0 #start position is vertical
nTrials = 100

win = visual.Window([800,800], monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True)


#Instructions text
instrText = visual.TextStim(win=win, ori=0, name='instrText',
    text=u'In this experiment you will observe a rotating white sphere and a flashed yellow sphere. Your objective is to indicate where the flashed yellow sphere appears relative to the rotating sphere. If it appears ahead of the white sphere, press the right arrow key, if it appears behind the white sphere, press the left arrow key, and if it appears at the same time, press the down arrow key. \n \n Press any key continue.',    font=u'Arial',
    pos=[0, 0], height=0.05, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)
InstructionsClock = core.Clock()


fixSpot = visual.GratingStim(win,tex=None, mask="gauss", size=(0.05,0.05),color='white', autoDraw=False)
clock = core.Clock() # to grab RTs, -- maybe make global?

clockDot = visual.GratingStim(win=win, mask="gauss", size=dotRad, color='white', opacity = '0.5', autoDraw=False)
flashDot = visual.GratingStim(win=win, mask="gauss", size=flashRad,color='yellow')

#Build vector of trialTypes
trialType = np.repeat([-20,-10,0,10,20],20)
myDict = {'-20': 'left', '-10': 'left', '0': 'down', '20': 'right', '10': 'right'}

randTrials = np.random.permutation(trialType)
response = [myDict[str(i)] for i in randTrials]
anglePres = np.arange(30,330,10)
values = [random.choice(anglePres) for _ in xrange(100)]
angle = np.arange(0,370,10)

#-------Set Up "Instructions"-------
NOT_STARTED = 0
STARTED=1
instructions_response = event.BuilderKeyResponse()  # create an object of type KeyResponse
instructions_response.status = NOT_STARTED
# keep track of which components have finished
InstructionsComponents = []
InstructionsComponents.append(instrText)
InstructionsComponents.append(instructions_response)
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Instructions"-------
frameN=0
continueRoutine = True
endExpNow=False
while continueRoutine:
    instrText.setAutoDraw(True)
    theseKeys = event.getKeys()
    if "escape" in theseKeys:
        endExpNow = True
    if len(theseKeys) > 0:  # at least one key was pressed
        continueRoutine = False
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
#-------End Routine "Instructions"-------


win.flip()
core.wait(3)
fixSpot.setAutoDraw(True)

#-------Start Routine "Main Experiment"-------
#ie forever Hard capped to 60Hz refresh rate
for rot, angleDev, response in zip(randTrials, values, response):
    #Check if user wants to quit
    if "escape" in theseKeys:
        core.quit()
    for angle in np.arange(0,370,10):
        angleRad = radians(angle)
        x = circleRadius*sin(angleRad)
        y = circleRadius*cos(angleRad)
        clockDot.setPos([x,y])
        clockDot.draw()

        if angle == angleDev:
            angleRad = radians(angle+rot)
            x = flashRadius*sin(angleRad)
            y = flashRadius*cos(angleRad)
            flashDot.setPos([x,y])
            flashDot.draw()
        win.flip()
        if event.getKeys(keyList="escape"):
            core.quit()
        event.clearEvents('mouse') #only really needed for pygame windows
    win.flip()

    theseKeys = event.waitKeys(float('inf'), keyList=('left', 'right', 'down', 'escape'), timeStamped = False)
    #Check if user wants to quit
    if "escape" in theseKeys:
        core.quit()
    key_response = theseKeys[0]
    #was the response correct?
    correct = key_response==response
    data_out.loc[len(data_out)+1]=[key_response,response, correct]
    data_out.to_csv(outputfn, index=False)
    core.wait(1)
#-------End Routine "Main Experiment"-------
