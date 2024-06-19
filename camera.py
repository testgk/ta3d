import math
from direct.task import Task
from panda3d.core import Point3

from cameracontroller import CameraController
from picker import Picker
from maps.terrainprovider import TerrainInfo


class TerrainCamera:
    def __init__(self, camera, mouseWatcherNode, camNode, render, terrainCenter: Point3 ):
        self.camera = camera
        self.__render = render
        self.mouseWatcherNode = mouseWatcherNode
        self.camNode = camNode
        self.__terrainCenter = terrainCenter
        self.__cameraHeight = None
        self.__cameraRadius = None
        self.__cameraAngle = None
        self.__terrainPicker = Picker( self.camera )
        self.setCamera()

    def setCamera( self ):
        self.__cameraAngle = 0  # Initial camera angle
        self.__cameraRadius = 1200  # Distance from the center of the terrain
        self.__cameraHeight = 400  # Height of the camera

    def rotateCamera( self, direction = 1 ):
        # Rotate the camera by a certain angle
        self.__cameraAngle += math.radians( direction * 10 )  # Rotate by 10 degrees per click
        self.updateCameraPosition()

    def hoverAbove(self ):
        self.__cameraAngle = 0  # Initial camera angle
        self.__cameraRadius = 0  # Distance from the center of the terrain
        self.__cameraHeight = 1200  # Height of the camera
        self.updateCameraPosition()

    def hoverDistance(self ):
        self.__cameraAngle = 0  # Initial camera angle
        self.__cameraRadius = 1200  # Distance from the center of the terrain
        self.__cameraHeight = 400  # Height of the camera
        self.updateCameraPosition()

    def updateCameraPosition( self ):
        camera_controller = CameraController( self.camera,
                                              self.__terrainCenter,
                                              cameraRadius = self.__cameraRadius,
                                              cameraHeight = self.__cameraHeight,
                                              cameraAngle = self.__cameraAngle )
        camera_controller.updateCameraPosition()


    def update_camera_task(self, task ):
        self.updateCameraPosition()
        return Task.cont  # Continue the task

    def on_map_click( self ):
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()

            # Set the position of the ray based on the mouse position
            self.__terrainPicker.pickerRay.setFromLens( self.camNode, mpos.getX(), mpos.getY() )

            # Perform the collision detection
            self.__terrainPicker.picker.traverse( self.__render )

            print( f"Mouse position: { mpos }" )  # Debugging
            print( f"Traversing collisions..." )  # Debugging

            numEntries = self.__terrainPicker.pickerQueue.getNumEntries()
            print( f"Number of collision entries: {numEntries}" )  # Debugging

            if numEntries > 0:
                # Sort entries so the closest is first
                self.__terrainPicker.pickerQueue.sortEntries()
                entry = self.__terrainPicker.pickerQueue.getEntry( 0 )
                point = entry.getSurfacePoint( self.__render )

                print( f"Collision detected at: {point}" )  # Debugging
                picked_obj = entry.getIntoNodePath()
                print( f"Clicked node ID or name: {picked_obj.getName()}" )
                # Update the terrain center to the clicked point
                self.__terrainCenter = point
                self.updateCameraPosition()
            else:
                print( "No collisions detected." )  # Debugging
