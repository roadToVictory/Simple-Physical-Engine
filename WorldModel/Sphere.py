from typing import Collection
from .Cuboid import Cuboid
from .Vector3D import Vector3D
import math
from .PhysicalObject import PhysicalObject
from kivy.graphics import Color, Ellipse
from WorldModel.World import World

class Sphere(PhysicalObject):
    def __init__(self, m,vec, r):
        self.radius = r
        PhysicalObject.__init__(self,vec, m,Vector3D(0,0,0),Vector3D(0,0,0))
        
    #function to draw sphere on canvas using dimensions dim1 and dim2
    def draw(self,canvas,dim1,dim2):
        with canvas:
            Color(self.color[1], self.color[2], self.color[3])
            Ellipse(pos=(World.toScreen(self.vector[dim1],1)-self.radius/2, World.toScreen(self.vector[dim2],2)-self.radius/2),size=(self.radius, self.radius))

    def setRadius(self, r):
        self.radius = r

    def __str__(self):
        return '[%s, %s, %s] r=%s' % (self.vector.x, self.vector.y, self.vector.z, self.radius)


#detect collision sphere with cuboid
def collission(sph, cuboid):
    minX, minY, minZ = cuboid.collect[0].x , cuboid.collect[0].y, cuboid.collect[0].z
    maxX, maxY, maxZ = cuboid.collect[0].x , cuboid.collect[0].y, cuboid.collect[0].z
    for i in range (1, 8):
        if cuboid.collect[i].x < minX: 
            minX = cuboid.collect[i].x
        elif cuboid.collect[i].x > maxX:
            maxX = cuboid.collect[i].x

        if cuboid.collect[i].y < minY: 
            minY = cuboid.collect[i].y
        elif cuboid.collect[i].y > maxY:
            maxY = cuboid.collect[i].y

        if cuboid.collect[i].z < minZ: 
            minZ = cuboid.collect[i].z
        elif cuboid.collect[i].z > maxZ:
            maxZ = cuboid.collect[i].z


    dx = max(minX, min(sph.vector.x, maxX))
    dy = max(minY, min(sph.vector.y, maxY))
    dz = max(minZ, min(sph.vector.z, maxZ))
    
    dr = math.sqrt(sph.vector.x**2 + sph.vector.y**2 + sph.vector.z**2)
    Long = 180/math.pi*math.atan2(sph.vector.y, sph.vector.x)   #longitude
    Lat = 180/math.pi*math.asin(sph.vector.z/dr)                #latitude 
    
    s2cX = dr*math.cos(Long/180*math.pi)*math.cos(Lat/180*math.pi)  ##spherical coord
    s2cY = dr*math.sin(Long/180*math.pi)*math.cos(Lat/180*math.pi)  ##spherical coord
    s2cZ = dr*math.sin(Lat/180*math.pi)                             ##spherical coord

    # phi=0
    # while phi<=2*math.pi:
    #     eta = math.pi * 2 / 3
    #     while eta <= math.pi:
    #         xx = sph.vector.x + sph.radius * math.sin(eta) * math.cos(phi)
    #         print(xx)
    #         eta += 1/100 * math.pi
    #     phi += 1/100 * math.pi
    
    #distance = math.sqrt( (dx - sph.vector.x) **2 + (dy - sph.vector.y) **2 + (dz - sph.vector.z) **2)

    distance = min(math.sqrt( (dx - sph.vector.x) **2 + (dy - sph.vector.y) **2 + (dz - sph.vector.z) **2), math.sqrt( (dx - s2cX) **2 + (dy - s2cY) **2 + (dz - s2cZ) **2))
  
    if distance <= sph.radius:
        return True
    else: return False
    