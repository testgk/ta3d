from direct.showbase.ShowBase import ShowBase
from panda3d.core import BitMask32, CollisionHandlerQueue, CollisionNode, CollisionPolygon, CollisionRay, \
    CollisionTraverser, \
    GeoMipTerrain, GeomVertexReader, Texture, \
    Filename, \
    PNMImage, Point3
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
        #self.disableMouse()
        self.create_rotate_left_button()
        self.create_rotate_right_button()
        self.create_above_button()
        self.create_distance_view_button()
        # Initialize camera rotation variables
        self.setCamera()
        self.terrain_size = terrainInfo.terrainSize
        self.terrain_center = terrainInfo.terrainCenter

        # Set up collision detection for mouse clicks
        self.picker = CollisionTraverser()
        self.pickerQueue = CollisionHandlerQueue()

        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(BitMask32.bit(1))
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.picker.addCollider(self.pickerNP, self.pickerQueue)
        self.accept( 'mouse1', self.on_map_click )
        self.create_terrain_collision()
        # Position the camera directly above the center of the terrain
        self.update_camera_position()

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
        self.update_camera_position()
        return Task.cont  # Continue the task

    def create_terrain_collision( self ):
        root = self.terrain.getRoot()
        geomNode = root.find( "**/+GeomNode" ).node()
        geom = geomNode.getGeom( 0 )
        vertexData = geom.getVertexData()

        format = geom.getVertexData().getFormat()
        vertexReader = GeomVertexReader( vertexData, 'vertex' )

        tris = geom.getPrimitive( 0 )
        tris = tris.decompose()

        vertexReader = GeomVertexReader( vertexData, 'vertex' )
        collisionNode = CollisionNode( 'terrain' )
        collisionNode.setIntoCollideMask( BitMask32.bit( 1 ) )

        for i in range( tris.getNumPrimitives() ):
            s = tris.getPrimitiveStart( i )
            e = tris.getPrimitiveEnd( i )
            assert e - s == 3

            vertices = [ ]
            for j in range( s, e ):
                vi = tris.getVertex( j )
                vertexReader.setRow( vi )
                v = vertexReader.getData3()
                vertices.append( v )

            poly = CollisionPolygon( vertices[ 0 ], vertices[ 1 ], vertices[ 2 ] )
            collisionNode.addSolid( poly )

        collisionNodePath = root.attachNewNode( collisionNode )
    def on_map_click(self):
        print('1111')
        if self.mouseWatcherNode.hasMouse():
            print( '222' )
            mpos = self.mouseWatcherNode.getMouse()

            # Set the position of the ray based on the mouse position
            self.pickerRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())

            # Perform the collision detection
            self.picker.traverse(self.render)

            if self.pickerQueue.getNumEntries() > 0:
                # Sort entries so the closest is first
                self.pickerQueue.sortEntries()
                entry = self.pickerQueue.getEntry(0)
                point = entry.getSurfacePoint(self.render)

                # Update the terrain center to the clicked point
                self.terrain_center = point
                self.update_camera_position()

app = MyApp()
app.run()
