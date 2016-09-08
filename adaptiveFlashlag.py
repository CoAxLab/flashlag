#!/usr/bin/env python2
#Author: P. Beukema February 2016
import math
import random
import pandas as pd
import numpy as np

import time
import os
import csv
import seaborn as sns
import matplotlib.pyplot as plt

from psychopy import visual, core, event, gui, data
from sklearn import linear_model

# Grab user info and set up output files for analysis
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
expName = 'FlashLagPilot'
expInfo = {u'User': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
outputfn =  _thisDir + os.sep +'data/%s_%s_%s.csv' %(expInfo['User'], \
            expName, expInfo['date'])
dataOut = pd.DataFrame(columns = ('rot','trials'))
grabMeans = pd.DataFrame()
deg_sign= u'\N{DEGREE SIGN}'

'''
Initalize stimuli parameters
all units are in pixels to show correctly on any sized screen
user may wish to modify for optimality on small or larger screens
tested on 1920x1080 (widescreen) display
'''

dotRad = (55,55)
flashRad = (55,55)
circleRadius = 125
flashRadius = circleRadius+35 # displacement from target in pixels

# Set up Window
win = visual.Window([1000,1000], monitor = 'testMonitor', color = [-1,-1,-1], \
       colorSpace = 'rgb', blendMode = 'avg', useFBO = True, allowGUI = \
       False,fullscr=True)

# Initalize Instructions Text
instructions = '====================================================== \n In this task, you will see two dots appear on the screen. The first dot will flash yellow in the bottom half of the screen. The second dot is white and will appear at the top center of your screen and move in a clockwise circle. \n \n Your objective is to move the yellow flashing dot at the bottom of the screen to be vertically aligned with the white dot at the 6 o-clock position. Use the left and right arrow keys to move the yellow dot in your desired direction. Pressing the left arrow key will rotate the flash clockwise (leftwards), pressing the right arrow key will rotate the flash anti-clockwise (rightwards).  \n \n The dot only moves slightly after each press, so you may have to hit the arrow keys multiple times before you notice any large movement. When you believe that the yellow and white dots are vertically aligned (at the 6 o-clock position), press the spacebar and the experiment will end.  ======================================================'
completedText = 'End of Testing. Thank you.'

instrText = visual.TextStim(win = win, ori = 0, name = 'instrText', text=instructions, font = u'Arial',  pos = [0, 0], height = 0.05, wrapWidth = None, color = u'white', colorSpace = 'rgb', opacity = 1, depth = 0.0)

expCompletedText = visual.TextStim(win = win, ori = 0, name = 'instrText', text=completedText, font = u'Arial',  pos = [0, 0], height = 0.05, wrapWidth = None, color = u'white', colorSpace = 'rgb', opacity = 1, depth = 0.0)


fixSpot = visual.GratingStim(win, tex = None, mask = 'gauss', size = (20,20), \
          units='pix', color = 'cyan', autoDraw = False)
clockDot = visual.GratingStim(win = win, mask = 'gauss', size = dotRad, \
           color = 'white', units='pix', opacity = '1', autoDraw=False)
flashDot = visual.GratingStim(win = win, mask = 'gauss', units='pix', \
           size = flashRad,color = 'yellow')


#-------Set Up Routine "Instructions"-------
notStarted = 0
started = 1
instructions_response = event.BuilderKeyResponse()
instructions_response.status = notStarted
InstructionsComponents = []
InstructionsComponents.append(instrText)
InstructionsComponents.append(instructions_response)
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = notStarted

#-------Start Routine "Instructions"-------
continueRoutine = True
endExpNow = False
while continueRoutine:
    instrText.setAutoDraw(True)
    theseKeys = event.getKeys()
    if 'escape' in theseKeys:
        endExpNow = True
    if len(theseKeys) > 0:
        continueRoutine = False
    if endExpNow or event.getKeys(keyList=['escape']):
        core.quit()
    if continueRoutine:
        win.flip()

for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, 'setAutoDraw'):
        thisComponent.setAutoDraw(False)

#-------End Routine "Instructions"-------
win.flip()
core.wait(.5)
fixSpot.setAutoDraw(False)


#-------End Routine "Practice"-------
win.flip()
core.wait(2)

#-------Start Routine "Main Experiment"-------
rot = -16
angleDev = 180
expComplete = 0
nTrials = 0 #to record how long it took subject to get to answer

while not expComplete:
    if 'escape' in theseKeys:
        core.quit()
    frameN = 0
    flash = False

    # project sphere for 800 ms so that user directs focus to sphere
    angleRad = math.radians(0)
    x = circleRadius*math.sin(angleRad)
    y = circleRadius*math.cos(angleRad)
    clockDot.setPos([x,y])
    clockDot.setAutoDraw(True)
    clockDot.draw()
    win.flip()
    core.wait(.8)

    for angle in np.arange(0,361,4):
        angleRad = math.radians(angle)
        x = circleRadius*math.sin(angleRad)
        y = circleRadius*math.cos(angleRad)
        clockDot.setPos([x,y])
        clockDot.draw()
        if angle == angleDev:
            angleMark = angle
            angleRad = math.radians(angleMark+rot)
            x2 = flashRadius*math.sin(angleRad)
            y2 = flashRadius*math.cos(angleRad)
            flash = True
        # set position of flash
        if frameN <= 1 and flash: # show flash for 1 frames
            flashDot.setPos([x2,y2])
            flashDot.draw()
            frameN = frameN+1
        win.flip()
        if event.getKeys(keyList ='escape'):
            core.quit()
        event.clearEvents('mouse')

    # Turn off stimulus and wait for response
    clockDot.setAutoDraw(False)
    win.update()
    win.flip()
    theseKeys = event.waitKeys(float('inf'), keyList=('left', 'right', 'escape', 'space'), timeStamped = False)

    # Check if user wants to quit
    if 'escape' in theseKeys:
        core.quit()

    key_response = theseKeys[0]
    print key_response
    # Check if the response was correct
    if key_response == 'left':
        rot += 2
    elif key_response == 'right':
        rot += -2
    elif key_response == 'space':
        expComplete = True
    nTrials += 1
    print nTrials
dataOut.loc[0] = [rot, nTrials]
dataOut.to_csv(outputfn, index = False)


#-------End Routine "Main Experiment"-------
expCompletedText.setAutoDraw(True)
win.flip()


#-------Set Up Routine "Experiment Complete"-------
notStarted = 0
started = 1
instructions3_response = event.BuilderKeyResponse()
instructions3_response.status = notStarted
InstructionsComponents3 = []
InstructionsComponents3.append(expCompletedText)
InstructionsComponents3.append(instructions_response)
for thisComponent in InstructionsComponents3:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = notStarted

#-------Start Routine "Instructions"-------
continueRoutine = True
endExpNow = False
while continueRoutine:
    expCompletedText.setAutoDraw(True)
    theseKeys = event.getKeys()
    if 'escape' in theseKeys:
        endExpNow = True
    if len(theseKeys) > 0:
        continueRoutine = False
    if endExpNow or event.getKeys(keyList=['escape']):
        core.quit()
    if continueRoutine:
        win.flip()

for thisComponent in InstructionsComponents3:
    if hasattr(thisComponent, 'setAutoDraw'):
        thisComponent.setAutoDraw(False)