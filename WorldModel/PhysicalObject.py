from .World import World
from .Vector3D import Vector3D
#Class representing a physical object with properties 
class PhysicalObject:
    def __init__(self, vec, m,a,v):
        self.vector= vec
        World.physicalObjects.append(self)
        self.color=Vector3D (1,1,0)
        self.mass = m
        self.accelerate = a
        self.velocity = v

    #function to set Color of the object, parameter is Vector3D
    def setColor(self,vect):
        self.color=vect.normalization()

    #stop object in 3D space
    def stabilize(self):
        self.accelerate=Vector3D(0,0,0)
        self.velocity=Vector3D(0,0,0)

    #set object position in 3D space
    def setPosition(self,pos):
        self.vector=pos

    def addPosition(self,pos):
        self.vector+=pos

    def getPosition(self):
        return self.vector

    #one step of movement - parameter is current acceleration
    def move(self,acc):
        self.accelerate=acc
        self.vector+=self.velocity
        self.velocity+=self.accelerate

    #empty function use to draw in inheritance classes
    def draw(self):
        pass
