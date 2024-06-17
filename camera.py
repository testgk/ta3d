import math
from direct.task import Task
from panda3d.core import Point3

from picker import Picker
from maps.terrainprovider import TerrainInfo



class TerrainCamera:
    def __init__(self, camera, mouseWatcherNode, camNode, render, terrainCenter: Point3 ):
        self.camera = camera
        self.render = render
        self.mouseWatcherNode = mouseWatcherNode
        self.camNode = camNode
        self.terrainCenter = terrainCenter
        self.cameraHeight = None
        self.cameraRadius = None
        self.cameraAngle = None
        self.terrainPicker = Picker( self.camera )
        self.setCamera()

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
        x = self.terrainCenter.getX() + ( self.cameraRadius or 1 ) * math.sin( self.cameraAngle )
        y = self.terrainCenter.getY() + ( self.cameraRadius or 1 ) * math.cos( self.cameraAngle )
        z = self.cameraHeight

        # Set camera position and orientation
        self.camera.setPos( x, y, z )
        self.camera.lookAt( self.terrainCenter )

    def update_camera_task(self, task ):
        self.updateCameraPosition()
        return Task.cont  # Continue the task

    def on_map_click( self ):
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()

            # Set the position of the ray based on the mouse position
            self.terrainPicker.pickerRay.setFromLens( self.camNode, mpos.getX(), mpos.getY() )

            # Perform the collision detection
            self.terrainPicker.picker.traverse( self.render )

            print( f"Mouse position: { mpos }" )  # Debugging
            print( f"Traversing collisions..." )  # Debugging

            numEntries = self.terrainPicker.pickerQueue.getNumEntries()
            print( f"Number of collision entries: {numEntries}" )  # Debugging

            if numEntries > 0:
                # Sort entries so the closest is first
                self.terrainPicker.pickerQueue.sortEntries()
                entry = self.terrainPicker.pickerQueue.getEntry( 0 )
                point = entry.getSurfacePoint( self.render )

                print( f"Collision detected at: {point}" )  # Debugging
                picked_obj = entry.getIntoNodePath()
                print( f"Clicked node ID or name: {picked_obj.getName()}" )
                # Update the terrain center to the clicked point
                self.terrainCenter = point
                self.updateCameraPosition()
            else:
                print( "No collisions detected." )  # Debugging
