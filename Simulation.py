from WorldModel.Vector3D import Vector3D, distance
from WorldModel.Cuboid import Cuboid
from WorldModel.Sphere import Sphere
from configparser import ConfigParser
from kivy.config import Config
from Parser import Parser
from WorldModel.World import World
import numpy as np
from WorldModel.Vector3D import Vector3D

class Simulation():
    def __init__(self):
        Parser.readAllData()
        Parser.recalculatedata()
        self.mainObject=Sphere(1,Vector3D(0,0,0),World.radius)
        self.shadow=Sphere(1,Vector3D(0,0,0),World.radius)
        self.corr=[2,6,8,9,10,15,22,29,31,36,37,39,41,44,46,53,56]


    def reset(self,game):
        self.arr=Parser.data[self.corr[game]]
        #print (self.arr)
        self.index=1
        self.mainObject.setPosition(Vector3D(0,0,0))
        self.shadow.setPosition(Vector3D(0,0,0))
        self.shadow.stabilize()
        self.mainObject.stabilize()
        self.mainObject.move(Vector3D.toVector(self.arr[0]))
        return np.array([self.mainObject.vector.x,self.mainObject.vector.y,self.mainObject.vector.z,self.mainObject.accelerate.x,self.mainObject.accelerate.y,self.mainObject.accelerate.z])

    def step(self,vect):
        vect=Vector3D(vect[0],vect[1],vect[2])
        self.shadow.addPosition(vect)
        #print(self.shadow.getPosition())
        self.mainObject.move(Vector3D.toVector(self.arr[self.index]))
        self.index+=1
        done=self.index+1==len(self.arr)
        dist=distance(self.mainObject.getPosition(),self.shadow.getPosition())
        return np.array([self.mainObject.vector.x,self.mainObject.vector.y,self.mainObject.vector.z,self.mainObject.accelerate.x,self.mainObject.accelerate.y,self.mainObject.accelerate.z]),-dist,done,False