from stimulate import cueInitial, stiInitial,onlinecueInitial,stiInitialalpha

import vizshape
import vizact
import viz
import viztask
import json
import logging
import vizinput
import sys,os
import time
import steamvr
import Queue
import threading
import numpy

#from telloVideo import telloVideo
#from tello import Tello



choice = vizinput.choose('Select Experiment Mode',['Online','Offline','Simulate Online'])


# Load the presettings file
presettingfile = open('PreSettings_Single.json')
settings = json.load(presettingfile)
stimulationLength = settings[u'stimulationLength'][0]
stimuliLoop = settings[u'stimuliLoop'][0]
frequence = settings[u'frequence']
phase = settings[u'phase']
size = settings[u'squaresize'][0]
keepsize = settings[u'keepsize'][0]
cuelen = settings[u'cuelen'][0]
textList = settings[u'controlCommand']
textposition = settings[u'textposition']
position = settings[u'position']
#framerate = settings[u'framerate'][0]
framerate = 60.0
cueseries =settings[u'cueSeries']

#Set the video window size

videoSquareSize = [12.8,7.2]
videoSquarePos = [0,0,19]
viz.setMultiSample(4)

pic = viz.addTexture('texture.jpg')


viz.window.setFullscreenMonitor(1)
viz.go(viz.FULLSCREEN)
viz.MainWindow.fov(60)
viz.MainView.setPosition(0,0,3)

attitudeDirector = viz.addChild('attitude.obj')
attitudeDirector.setPosition(0,0,14)
attitudeDirector.color([0,1,0])
attitudeDirector.setAxisAngle([0,1,0, 90])
attitudeDirector.setScale([0.2,0.2,0.2])
attitudeDirector.visible(viz.ON)

quadBack = viz.addTexQuad(size=videoSquareSize)
quadBack.setPosition(videoSquarePos)

quadBack.texture(pic) 


# Gird on the video:
viz.startLayer(viz.LINES)
viz.vertexColor(1,0,0)
viz.vertex(6.4,3.6,18.9)
viz.vertex(3.2,1.8,18.9)
viz.vertex(3.2,1.8,18.9)
viz.vertex(-3.2,1.8,18.9)
viz.vertex(-3.2,1.8,18.9)
viz.vertex(-6.4,3.6,18.9)
viz.vertex(6.4,-3.6,18.9)
viz.vertex(3.2,-1.8,18.9)
viz.vertex(3.2,-1.8,18.9)
viz.vertex(-3.2,-1.8,18.9)
viz.vertex(-3.2,-1.8,18.9)
viz.vertex(-6.4,-3.6,18.9)
viz.vertex(4.8,2.7,18.9)
viz.vertex(-4.8,2.7,18.9)
viz.vertex(4.8,-2.7,18.9)
viz.vertex(-4.8,-2.7,18.9)
viz.vertexColor(0,1,0)
viz.vertex(6.4,0,18.9)
viz.vertex(-6.4,0,18.9)
viz.vertex(0,3.6,18.9)
viz.vertex(0,-3.6,18.9)
gridLines = viz.endLayer()


squares = {}
fbsquares = {}
for i in range(len(position)):
	if i<=11 and i!=10:
		squares['square'+str(i)] = vizshape.addBox(size=(size,size,0.01), splitFaces=False, pos=position[str(i)])
		#fbsquares['fbsquare'+str(i)] = vizshape.addQuad(size=(size+0.1,size+0.1), pos = position[str(i)],color = (0,0,0))
	else:
		squares['square'+str(i)] = vizshape.addBox(size=(keepsize,keepsize,0.01), splitFaces=False, pos=position[str(i)])
		#fbsquares['fbsquare'+str(i)] = vizshape.addQuad(size=(keepsize+0.1,keepsize+0.1), pos = position[str(i)],color = (1,1,1 ))

texts = {}
#Set text showing on the squares
for i in range(len(position)):
	if i<=11 and i!=10:
		texts['text'+str(i)] = viz.addText(textList[str(i)].encode('utf-8'),parent=squares['square'+str(i)],pos=[0,0,-0.1])
		texts['text'+str(i)].font('Times New Roman')
		texts['text'+str(i)].color(viz.BLACK)
		texts['text'+str(i)].setScale([0.4,0.4,0.4])
		texts['text'+str(i)].alignment(viz.TEXT_CENTER_CENTER)

readyAnswer = vizinput.ask("If ready, press 'Yes'")

# define a task sequence, stimulate action will execute until cue finish
triggersignal = viztask.Signal()
def stistage():
	for i in range(len(position)):
		if i<=11 and i!=10:
			squares['square'+str(i)].addAction(stiInitial(stimulationLength,frequence[i],phase[i],framerate))
		else:
			squares['square'+str(i)].addAction(stiInitial(stimulationLength,frequence[10],phase[10],framerate))
	yield None
	
def triggerWrite(msg):
	pass
		
if choice == 1:
	def mytask():
		shortcue = onlinecueInitial(0.01)
		cue = cueInitial(cuelen)
		for cueLoop in range(len(cueseries)):
			series = cueseries[cueLoop]
			for i in series:
				yield viztask.addAction(squares['square'+str(i)],cue)
				#myserial.serialWrite((i+1))
				triggerWrite(i)
				yield stistage()
				yield viztask.addAction(squares['square'+str(1)],shortcue)
				triggerWrite(i)
				yield stistage()
				yield viztask.addAction(squares['square'+str(1)],shortcue)
				triggerWrite(i)
				yield stistage()
				yield viztask.addAction(squares['square'+str(1)],shortcue)
				triggerWrite(i)
				yield stistage()
				yield viztask.addAction(squares['square'+str(1)],shortcue)
				triggerWrite(i)
				yield stistage()
	viztask.schedule(mytask())
	
elif choice == 0:
	def mytask():
		counter = 0
		while True:
			counter+=1
			cue = onlinecueInitial(0.01)

			#serial.serialWrite(counter)
			yield viztask.addAction(squares['square'+str(1)],cue)
			yield stistage()
			if counter > 250:
				counter = 0
	viztask.schedule(mytask())
	 
elif choice == 2: 
	def mytask():
		triggerSeries = [0,1,2,3,4,5,6,7,8,9,10,11,1,3,5,7,9,11,2,4,6,8,10]
		for triggernum in triggerSeries:
			counter = 0
			currentpos = position[str(triggernum)]
			trigger = vizshape.addSphere(radius=0.15,slices=20,stacks=20,axis=vizshape.AXIS_Y, pos = [currentpos[0],currentpos[1]-0.9,currentpos[2]])
			trigger.color(viz.RED)
			while True:
				counter+=1
				cue = onlinecueInitial(0.01)

				#serial.serialWrite(counter)
				yield viztask.addAction(squares['square'+str(1)],cue)
				triggerWrite(i)
				yield stistage()
				if counter >= 10:
					break
			trigger.remove()
	viztask.schedule(mytask())

	

'''
	Necessary test examples are saved below
'''
