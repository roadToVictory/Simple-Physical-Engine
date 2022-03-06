from WorldModel.Vector3D import Vector3D
from WorldModel.Cuboid import Cuboid
from WorldModel.Sphere import Sphere
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
from configparser import ConfigParser
from kivy.config import Config
from Parser import Parser
from WorldModel.World import World
from kivy.uix.label import Label
import numpy as np
from math import sin
from math import cos

class VisualizationApp(Widget):
	def __init__(self,**kwargs):
		Config.set('graphics', 'width', World.width)
		Config.set('graphics', 'height', World.height)
		Parser.readAllData()
		Parser.recalculatedata()
		Parser.readGenData()
		self.itr=0
		super(VisualizationApp,self).__init__(**kwargs)
		self.floor=Cuboid(100,Vector3D(10000,10000,-800),Vector3D(10000,-10000,-800),Vector3D(-10000,-10000,-800),Vector3D(-10000,10000,-800),Vector3D(10000,10000,-900),Vector3D(10000,-10000,-900),Vector3D(-10000,-10000,-900),Vector3D(-10000,10000,-900))
		self.mainObject=Sphere(1,Vector3D(0,0,1000),World.radius)
		self.shadowObject=Sphere(1,Vector3D(0,0,1000),World.radius)
		self.shadowObject.setColor(Vector3D(0,0,1))
		# 6,8,9,10,15,36,37,39,41,44,46,53,56]
		self.testarr=Parser.data[2]
		self.ind=0
		self.shadowArray=Parser.gendata[self.ind]
		if len(self.testarr)<len(self.shadowArray):
			self.limit=len(self.testarr)
		else:
			self.limit=110
		self.cursor=0
		Clock.schedule_interval(self.refresh, 1/int(World.framerate))
    	
	def refresh(self,dt):
		self.canvas.clear()
		if self.cursor<self.limit:
			self.mainObject.move(Vector3D.toVector(self.testarr[self.cursor]))
			self.shadowObject.move(Vector3D.toVector(self.shadowArray[self.cursor]).reverse())
			self.cursor+=1
		else:
			self.cursor=0
			self.ind+=1
			self.shadowArray=Parser.gendata[self.ind]
			self.mainObject.setPosition(Vector3D(0,0,1000))
			self.mainObject.stabilize()
			self.shadowObject.stabilize()
			self.shadowObject.setPosition(Vector3D(0,0,1000))
			self.itr+=10
			if(self.itr>=len(Parser.gendata)):
				self.itr=0
			self.shadowArray=Parser.gendata[self.itr]
		for i in World.physicalObjects:
			i.draw(self.canvas,1,3)
		with self.canvas:
			l = Label(text=str(self.itr), font_size='50sp')

class VisualApp(App):
     def build(self):
         return VisualizationApp()

if __name__ == '__main__':
     VisualApp().run()