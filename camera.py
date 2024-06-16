import math
from direct.task import Task

from maps.terrainprovider import TerrainInfo


class TerCamera:
    def __init__(self, camera, terrainInfo: TerrainInfo ):
        self.camera = camera
        self.terrainCenter = terrainInfo.terrainCenter
        self.cameraHeight = None
        self.cameraRadius = None
        self.cameraAngle = None

    def setCamera( self ):
        self.cameraAngle = 0  # Initial camera angle
        self.cameraRadius = 1200  # Distance from the center of the terrain
        self.cameraHeight = 400  # Height of the camera

    def rotateCamera( self, direction = 1 ):
        # Rotate the camera by a certain angle
        self.cameraAngle += math.radians( direction * 10 )  # Rotate by 10 degrees per click
        self.updateCameraPosition()

    def hoverAbove(self ):
        self.cameraAngle = 0  # Initial camera angle
        self.cameraRadius = 0  # Distance from the center of the terrain
        self.cameraHeight = 1200  # Height of the camera
        self.updateCameraPosition()

    def hoverDistance(self ):
        self.cameraAngle = 0  # Initial camera angle
        self.cameraRadius = 1200  # Distance from the center of the terrain
        self.cameraHeight = 400  # Height of the camera
        self.updateCameraPosition()

    def updateCameraPosition( self ):
        # Calculate new camera position on a circular path around the terrain center
        x = self.terrainCenter.getX() + (self.cameraRadius or 1) * math.sin( self.cameraAngle )
        y = self.terrainCenter.getY() + (self.cameraRadius or 1) * math.cos( self.cameraAngle )
        z = self.cameraHeight

        # Set camera position and orientation
        self.camera.setPos( x, y, z )
        self.camera.lookAt( self.terrainCenter )

    def update_camera_task(self, task ):
        self.updateCameraPosition()
        return Task.cont  # Continue the task
