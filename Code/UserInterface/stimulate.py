import viz
import vizshape
import numpy as np

def GenFilckerCode(stimultLegth, frequence, refreshRate, phase):
	index = np.arange(int(stimultLegth*refreshRate))
	temp = np.sin(2*np.pi*frequence*(index/refreshRate)+phase*np.pi)
	code = (temp+1)/2
	return code


class cueAction(viz.ActionClass):
	'''
	Define cue action by inherit the ActionClass 
	'''
	
	def begin(self,object):
		
		self.cueDuration = self._actiondata_.data[0]
		
		self.timeElapsed = 0
		self.counter = 0
		
	def update(self,elapsed,object):
		self.timeElapsed += elapsed
		self.counter += 1
		object.alpha(1)
		
		if self.cueDuration>0.0 and self.timeElapsed>self.cueDuration:
			# The end condition of square
			object.color([1,1,1])
			self.end(object)
			
		else:
			object.color([1,0,0])

# Initial cue action, this function offer access to cue action
# and use addaction to a vizard object.
def cueInitial(cueDuration = 2):
	action = viz.ActionData()
	action.data = [cueDuration]
	action.actionclass = cueAction
	return action
			
		


class stiAction(viz.ActionClass):
	'''
	Define stimulate action by inherit the ActionClass 
	'''
	
	def begin(self,object):
		
		self.stiDuration = self._actiondata_.data[0]
		self.frequence = self._actiondata_.data[1]
		self.phase = self._actiondata_.data[2]
		self.refreshRate = self._actiondata_.data[3]

		self.code = GenFilckerCode(self.stiDuration,self.frequence,self.refreshRate,self.phase)
		
		self.counter = 0
	
	def update(self,elapsed,object):
		
		if self.counter>=len(self.code):
			object.color([1,1,1])
			self.end(object)
		else:
			colorSet = self.code[self.counter]
			object.color([colorSet,colorSet,colorSet])
			self.counter = self.counter+1

# Initial stimulate action, this function offer access to cue action
# and use addaction to a vizard object.
def stiInitial(stiDuration ,frequence,phase,refreshRate):
	action = viz.ActionData()
	action.data = [stiDuration,frequence,phase,refreshRate]
	action.actionclass = stiAction
	return action

class stiActionalpha(viz.ActionClass):
	'''
	Define stimulate action by inherit the ActionClass 
	'''
	
	def begin(self,object):
		
		self.stiDuration = self._actiondata_.data[0]
		self.frequence = self._actiondata_.data[1]
		self.phase = self._actiondata_.data[2]
		self.refreshRate = self._actiondata_.data[3]

		self.code = GenFilckerCode(self.stiDuration,self.frequence,self.refreshRate,self.phase)
		
		self.counter = 0
	
	def update(self,elapsed,object):
		
		if self.counter>=len(self.code):
			object.color([1,1,1])
			self.end(object)
		else:
			object.alpha(1)
			colorSet = self.code[self.counter]
			object.color([colorSet,colorSet,colorSet])
			if colorSet < 0.5:
				object.alpha(0)
			self.counter = self.counter+1

# Initial stimulate action, this function offer access to cue action
# and use addaction to a vizard object.
def stiInitialalpha(stiDuration ,frequence,phase,refreshRate):
	action = viz.ActionData()
	action.data = [stiDuration,frequence,phase,refreshRate]
	action.actionclass = stiActionalpha
	return action
	

class onlinecueAction(viz.ActionClass):
	'''
	Define cue action by inherit the ActionClass 
	'''
	
	def begin(self,object):
		
		self.cueDuration = self._actiondata_.data[0]
		
		self.timeElapsed = 0
		self.counter = 0
		
	def update(self,elapsed,object):
		self.timeElapsed += elapsed
		self.counter += 1
		
		if self.cueDuration>0.0 and self.timeElapsed>self.cueDuration:
			# The end condition of square
			object.color([1,1,1])
			self.end(object)
			
		else:
			object.color([1,1,1])



# Initial cue action, this function offer access to cue action
# and use addaction to a vizard object.
def onlinecueInitial(cueDuration = 2):
	action = viz.ActionData()
	action.data = [cueDuration]
	action.actionclass = onlinecueAction
	return action