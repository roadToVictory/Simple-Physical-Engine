from configparser import ConfigParser
from .Vector3D import Vector3D
cfg=ConfigParser()
cfg.read('app_config.ini')
cfg.sections()

#stores all object of class PhysicalObject - draw
class World():
    physicalObjects=[]
    minbound=int(cfg.get('world','minbound'))
    maxbound=int(cfg.get('world','maxbound'))
    width=int(cfg.get('visual','width'))
    height=int(cfg.get('visual','height'))
    framerate=int(cfg.get('visual','framerate'))
    radius=int(cfg.get('ball','radius'))
    dim=[width,height]

    #calculate from world position to screen position
    @staticmethod
    def toScreen(x,cord):
        return ((x-World.minbound)/(World.maxbound-World.minbound))*World.dim[cord-1]