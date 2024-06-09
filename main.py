from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain, Texture, Filename, PNMImage, Point3
from direct.gui.DirectGui import DirectButton
from direct.task import Task
import math

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Create the terrain
        self.create_terrain()

        # Disable default mouse-based camera control
        self.disableMouse()

        # Add a button to rotate the camera
        self.create_rotate_button()

        # Initialize camera rotation variables
        self.camera_angle = 0  # Initial camera angle
        self.camera_radius = 900  # Distance from the center of the terrain
        self.camera_height = 400  # Height of the camera

        # Position the camera directly above the center of the terrain
        self.update_camera_position()

        # Start a task to update the camera position
        self.taskMgr.add(self.update_camera_task, "UpdateCameraTask")

    def create_terrain(self):
        # Create a GeoMipTerrain object
        self.terrain = GeoMipTerrain("terrain")

        # Load the heightmap
        heightmap = PNMImage(Filename("maps/heightmap.png"))
        self.terrain.setHeightfield(heightmap)

        # Set terrain properties
        self.terrain.setBlockSize(32)
        self.terrain.setNear(40)
        self.terrain.setFar(200)
        self.terrain.setFocalPoint(self.camera)

        # Generate the terrain
        self.terrain.generate()

        # Apply a texture to the terrain
        texture = self.loader.loadTexture("maps/terrain_texture.png")
        self.terrain.getRoot().setTexture(texture)

        # Reparent the terrain to the render node
        self.terrain.getRoot().reparentTo(self.render)

        # Enable the terrain's LOD (Level of Detail) system
        self.terrain.getRoot().setSz(100)

        # Calculate the center of the terrain
        self.terrain_size = heightmap.getXSize()  # Assuming square heightmap
        self.terrain_center = Point3(self.terrain_size / 2, self.terrain_size / 2, 0)

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
