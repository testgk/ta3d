from panda3d.core import Vec3
from direct.interval.LerpInterval import LerpPosInterval, LerpHprInterval
from direct.interval.IntervalGlobal import Sequence
import math


class CameraController:
    def __init__( self, camera, terrainCenter, cameraRadius = 10, cameraHeight = 10, cameraAngle = 0,
                  transitionTime = 0.1 ):
        self.camera = camera
        self.__terrainCenter = terrainCenter
        self.__cameraRadius = cameraRadius
        self.__cameraHeight = cameraHeight
        self.__cameraAngle = cameraAngle
        self.__transitionTime = transitionTime

    def updateCameraPosition( self ):
        # Calculate new camera position on a circular path around the terrain center
        x = self.__terrainCenter.getX() + ( self.__cameraRadius or 1 ) * math.sin( self.__cameraAngle )
        y = self.__terrainCenter.getY() + ( self.__cameraRadius or 1 ) * math.cos( self.__cameraAngle )
        z = self.__cameraHeight

        # Target position
        targetPos = Vec3( x, y, z )

        # Set camera to look at the terrain center to calculate the target HPR
        self.camera.lookAt( self.__terrainCenter )

        # Get the target HPR (heading, pitch, roll)
        targetHpr = self.camera.getHpr()

        # Reset the camera to its original orientation to avoid immediate jump
        self.camera.setHpr( targetHpr )

        # Create interpolation intervals
        posInterval = LerpPosInterval( self.camera, self.__transitionTime, targetPos )
        hprInterval = LerpHprInterval( self.camera, self.__transitionTime, targetHpr )

        # Create and play a sequence of these intervals
        cameraMove = Sequence( posInterval, hprInterval )

        cameraMove.start()