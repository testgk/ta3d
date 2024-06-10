from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain, Texture, Filename, PNMImage, Point3
from direct.gui.DirectGui import DirectButton
from direct.task import Task
import math

from maps.terrainprovider import TerrainProvider


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        terrainProvider = TerrainProvider( self.loader )
        terrainInfo = terrainProvider.create_terrain( "heightmap" )
        self.terrain = terrainInfo.terrain
        self.terrain.getRoot().reparentTo( self.render )
        self.terrain.setFocalPoint( self.camera )
        self.disableMouse()
        self.create_rotate_button()
        # Initialize camera rotation variables
        self.camera_angle = 0  # Initial camera angle
        self.camera_radius = 900  # Distance from the center of the terrain
        self.camera_height = 400  # Height of the camera
        self.terrain_size = terrainInfo.terrainSize
        self.terrain_center = terrainInfo.terrainCenter

        # Position the camera directly above the center of the terrain
        self.update_camera_position()
        # Start a task to update the camera position
        self.taskMgr.add(self.update_camera_task, "UpdateCameraTask")

    def create_rotate_button(self):
        # Create a button to rotate the camera
        rotate_button = DirectButton(
            text="Rotate Camera",
            command=self.rotate_camera,
            pos=(0, 0, -0.9),
            scale=0.1
        )

    def rotate_camera(self):
        # Rotate the camera by a certain angle
        self.camera_angle += math.radians(10)  # Rotate by 10 degrees per click
        self.update_camera_position()

    def update_camera_position(self):
        # Calculate new camera position on a circular path around the terrain center
        x = self.terrain_center.getX() + self.camera_radius * math.sin(self.camera_angle)
        y = self.terrain_center.getY() + self.camera_radius * math.cos(self.camera_angle)
        z = self.camera_height

        # Set camera position and orientation
        self.camera.setPos(x, y, z)
        self.camera.lookAt(self.terrain_center)

    def update_camera_task(self, task):
        # Update the camera position continuously if needed (e.g., for animation)
        self.update_camera_position()
        return Task.cont  # Continue the task

app = MyApp()
app.run()
