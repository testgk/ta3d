from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain, Texture, Filename, PNMImage, Point3
from direct.gui.DirectGui import DirectButton
from direct.task import Task
import math

from maps.terrainprovider import TerrainProvider


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.camera_height = None
        self.camera_radius = None
        self.camera_angle = None
        terrainProvider = TerrainProvider( self.loader )
        terrainInfo = terrainProvider.create_terrain( "heightmap" )
        self.terrain = terrainInfo.terrain
        self.terrain.getRoot().reparentTo( self.render )
        self.terrain.setFocalPoint( self.camera )
        self.disableMouse()
        self.create_rotate_left_button()
        self.create_rotate_right_button()
        self.create_above_button()
        self.create_distance_view_button()
        # Initialize camera rotation variables
        self.setCamera()
        self.terrain_size = terrainInfo.terrainSize
        self.terrain_center = terrainInfo.terrainCenter

        # Position the camera directly above the center of the terrain
        self.update_camera_position()
        # Start a task to update the camera position
        self.taskMgr.add(self.update_camera_task, "UpdateCameraTask")

    def setCamera( self ):
        self.camera_angle = 0  # Initial camera angle
        self.camera_radius = 1200  # Distance from the center of the terrain
        self.camera_height = 400  # Height of the camera

    def create_rotate_left_button(self):
        rotate_button = DirectButton(
            text="Rotate Left",
            command=self.rotate_camera,
            pos=(0, 0, -0.9),
            scale=0.1
        )

    def create_rotate_right_button(self):
        rotate_button = DirectButton(
            text="Rotate Right",
            command=self.rotate_camera,
            pos=(0, 0, 0.9),
            scale=0.1,
            extraArgs=[ -1 ]
        )

    def create_above_button( self ):
        rotate_button = DirectButton(
            text = "Hover Above",
            command = self.hover_above,
            pos = (0.9, 0.9, 0),
            scale = 0.1
        )

    def create_distance_view_button( self ):
        rotate_button = DirectButton(
            text = "Distance View",
            command = self.hover_distance,
            pos = (-0.9, -0.9, 0),
            scale = 0.1
        )

    def rotate_camera(self, direction = 1 ):
        # Rotate the camera by a certain angle
        self.camera_angle += math.radians( direction * 10)  # Rotate by 10 degrees per click
        self.update_camera_position()

    def hover_above(self ):
        self.camera_angle = 0  # Initial camera angle
        self.camera_radius = 0  # Distance from the center of the terrain
        self.camera_height = 1200  # Height of the camera
        self.update_camera_position()

    def hover_distance(self ):
        self.camera_angle = 0  # Initial camera angle
        self.camera_radius = 1200  # Distance from the center of the terrain
        self.camera_height = 400  # Height of the camera
        self.update_camera_position()

    def update_camera_position(self):
        # Calculate new camera position on a circular path around the terrain center
        x = self.terrain_center.getX() + ( self.camera_radius or 1 ) * math.sin(self.camera_angle)
        y = self.terrain_center.getY() + ( self.camera_radius or 1 )  * math.cos(self.camera_angle)
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
