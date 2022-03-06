from WorldModel.Vector3D import Vector3D
from math import sqrt
from .PhysicalObject import PhysicalObject
from kivy.graphics import Color, Rectangle
from WorldModel.World import World

#class of vector in three dimensions space
class Cuboid(PhysicalObject):
    def __init__(self, m,*args):
        self.collect=[]
        center=Vector3D (0,0,0)
        self.minpoint=Vector3D(1000000,1000000,1000000)
        self.maxpoint=Vector3D(-1000000,-1000000,-1000000)
        for x in args:
            if x not in self.collect:   #checking the uniqueness of vectors
                self.maxpoint.x=max(self.maxpoint.x,x.x)
                self.maxpoint.y=max(self.maxpoint.y,x.y)
                self.maxpoint.z=max(self.maxpoint.z,x.z)
                self.minpoint.x=min(self.minpoint.x,x.x)
                self.minpoint.y=min(self.minpoint.y,x.y)
                self.minpoint.z=min(self.minpoint.z,x.z)
                self.collect.append(x)
                center+=x
        self.size=self.maxpoint-self.minpoint
        center.x=center.x/4
        center.y=center.y/4
        center.z=center.z/4
        PhysicalObject.__init__(self,center, m,Vector3D(0,0,0),Vector3D(0,0,0))
        self.color=Vector3D (0,1,0)

    #function to draw sphere on canvas using dimensions dim1 and dim2
    def draw(self,canvas,dim1,dim2):
        with canvas:
            Color(self.color[1], self.color[2], self.color[3])
            Rectangle(pos=(World.toScreen(self.vector[dim1],1)-self.size[dim1]/2,World.toScreen(self.vector[dim2],2)-self.size[dim2]/2),size=(self.size[dim1], self.size[dim2]))

    def __str__(self):
        for i in self.collect:
            print(i)
        return ""
