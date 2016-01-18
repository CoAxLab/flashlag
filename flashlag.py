#!/usr/bin/env python2

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

#Grab user info and set up output files for analysis
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
expName = 'FlashLagPilot'
expInfo = {u'User': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
outputfn =  _thisDir + os.sep +'data/%s_%s_%s.csv' %(expInfo['User'], expName, expInfo['date'])
dataOut = pd.DataFrame(columns = ('response','correct','rotation'))
grabMeans = pd.DataFrame()

#Initalize stimuli parameters
#all units are in pixels to show correctly on any sized screen
#user may wish to modify for optimality on small or larger screens
#tested on 1920x1080 (widescreen) display
dotRad = (25,25)
flashRad = (25,25)
circleRadius = 200
flashRadius = circleRadius+25 # displacement from target in pixels

#Set up Window
win = visual.Window([1000,1000], monitor = 'testMonitor', color = [-1,-1,-1], colorSpace = 'rgb', blendMode = 'avg', useFBO = True, allowGUI = False,fullscr=True)

#Initalize Instructions Text
instrText = visual.TextStim(win = win, ori = 0, name = 'instrText',
    text=u'In this experiment you will observe a rotating white sphere and a flashed yellow sphere. If the flash appears ahead of the white sphere, press \u2190, if it appears behind the white sphere, press \u2192. \n \n Press any key continue.', font = u'Arial',  pos = [0, 0], height = 0.05, wrapWidth = None, color = u'white', colorSpace = 'rgb', opacity = 1, depth = 0.0)

fixSpot = visual.GratingStim(win, tex = None, mask = 'gauss', size = (20,20), units='pix', color = 'white', autoDraw = False)
clockDot = visual.GratingStim(win = win, mask = 'gauss', size = dotRad, color = 'white', units='pix', opacity = '0.9', autoDraw=False)
flashDot = visual.GratingStim(win = win, mask = 'gauss', units='pix', size = flashRad,color = 'yellow')

#Build vector of trials, dynamically generated for each new user
trialType = np.repeat([-20,0,20,40,60],20)
myDict = {'-20': 'right', '0': 'right', '20': 'left', '40': 'left', '60': 'left'}
randTrials = np.random.permutation(trialType)
response = [myDict[str(i)] for i in randTrials]
anglePres = np.arange(90,210,10) # yellow flash
values = [random.choice(anglePres) for _ in xrange(100)]

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
core.wait(3)
fixSpot.setAutoDraw(False)

#-------Start Routine "Main Experiment"-------
for rot, angleDev, response in zip(randTrials, values, response):
    if 'escape' in theseKeys:
        core.quit()
    frameN = 0
    flash = False

    #project sphere for 500 ms so that user directs focus to sphere
    angleRad = math.radians(0)
    x = circleRadius*math.sin(angleRad)
    y = circleRadius*math.cos(angleRad)
    clockDot.setPos([x,y])
    clockDot.setAutoDraw(True)
    clockDot.draw()
    win.flip()
    core.wait(.8)


    for angle in np.arange(0,361,5):
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
        #set position of flash
        if frameN <= 4 and flash:
            flashDot.setPos([x2,y2])
            flashDot.draw()
            frameN = frameN+1
        win.flip()
        if event.getKeys(keyList ='escape'):
            core.quit()
        event.clearEvents('mouse')

    #turn off stimulus and wait for response
    clockDot.setAutoDraw(False)
    win.update()
    win.flip()
    theseKeys = event.waitKeys(float('inf'), keyList=('left', 'right', 'escape'), timeStamped = False)
    #Check if user wants to quit
    if 'escape' in theseKeys:
        core.quit()

    key_response = theseKeys[0]
    #was the response correct?
    correct = key_response == response
    dataOut.loc[len(dataOut)+1] = [key_response, correct, rot]
    dataOut.to_csv(outputfn, index = False)

    core.wait(.5)
#-------End Routine "Main Experiment"-------

#-------Analyze Data To do: Fit Logit model----

#grabMeans = dataOut.groupby(['rotation'], as_index=False).mean()
grabMeans = pd.DataFrame(columns=('rotation', 'accuracy'))
i = 0
for rot in np.unique(dataOut[['rotation']]):
    block_df = dataOut.loc[dataOut['rotation']==rot]
    mean_acc = block_df[['correct']].mean()
    grabMeans.loc[i] = [rot, mean_acc.correct]
    i = i + 1
plt.figure(figsize=(6,6))
sns.regplot(x='rotation', y='accuracy', data = grabMeans, fit_reg = False)
plotfn =  _thisDir + os.sep +'data/%saccuracy_%s_.png' %(expInfo['User'], expName)
plt.savefig(plotfn)
