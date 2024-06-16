
from camera import TerCamera
from camerabuttons import CameraButtons
from direct.showbase.ShowBase import ShowBase
from maps.terrainprovider import TerrainProvider
from panda3d.core import BitMask32, CollisionHandlerQueue, CollisionNode, CollisionPolygon, CollisionRay, \
    CollisionTraverser, GeomNode, GeomVertexReader


class MyApp(ShowBase):
    def __init__( self ):
        ShowBase.__init__( self )
        self.pickerQueue = None
        self.picker = None
        self.pickerRay = None
        self.pickerNP = None
        self.pickerNode = None
        terrainProvider = TerrainProvider( self.loader )
        terrainInfo = terrainProvider.create_terrain( "heightmap1" )
        self.terrain = terrainInfo.terrain
        self.terrain.getRoot().reparentTo( self.render )
        self.terrain.setFocalPoint( self.camera )
        self.disableMouse()
        self.trCamera = TerCamera( self.camera, terrainInfo )
        self.cameraButtons = CameraButtons( self.trCamera )
        self.trCamera.terrainCenter = terrainInfo.terrainCenter
        self.trCamera.setCamera()
        self.createPicker()
        self.accept( 'mouse1', self.on_map_click )
        # Create a collision mesh for the terrain
        self.create_terrain_collision()
        # Start a task to update the camera position
        self.taskMgr.add( self.trCamera.update_camera_task, "UpdateCameraTask" )

    def createPicker( self ):
        # Set up collision detection for mouse clicks
        self.picker = CollisionTraverser()
        self.pickerQueue = CollisionHandlerQueue()
        self.pickerNode = CollisionNode( 'mouseRay' )
        self.pickerNP = self.camera.attachNewNode( self.pickerNode )
        self.pickerNode.setFromCollideMask( BitMask32.bit( 1 ) )
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid( self.pickerRay )
        self.picker.addCollider( self.pickerNP, self.pickerQueue )

    def create_terrain_collision(self):
        # Assuming self.terrain is your terrain NodePath
        root = self.terrain.getRoot()

        # Iterate over each GeomNode
        for child in root.getChildren():
            if isinstance( child.node(), GeomNode ):
                geom_node = child.node()
                geom = geom_node.getGeom( 0 )  # Assuming each GeomNode has one Geom
                vertex_data = geom.getVertexData()

                tris = geom.getPrimitive( 0 )  # Assuming the first primitive is triangles
                tris = tris.decompose()

                collision_node = CollisionNode(f'terrain_{child.getName()}')
                collision_node.setIntoCollideMask(BitMask32.bit(1))

                vertex_reader = GeomVertexReader(vertex_data, 'vertex')

                for i in range(tris.getNumPrimitives()):
                    s = tris.getPrimitiveStart(i)
                    e = tris.getPrimitiveEnd(i)
                    assert e - s == 3

                    vertices = []
                    for j in range(s, e):
                        vi = tris.getVertex(j)
                        vertex_reader.setRow(vi)
                        v = vertex_reader.getData3()
                        vertices.append(v)

                    poly = CollisionPolygon(vertices[0], vertices[1], vertices[2])
                    collision_node.addSolid(poly)

                collision_node_path = child.attachNewNode(collision_node)
                collision_node_path.show()  # Show the collision node for debugging

                print(f"Collision node { child.getName() } created and attached to terrain")  # Debugging

    def on_map_click( self ):
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()

            # Set the position of the ray based on the mouse position
            self.pickerRay.setFromLens( self.camNode, mpos.getX(), mpos.getY() )

            # Perform the collision detection
            self.picker.traverse( self.render )

            print( f"Mouse position: { mpos }" )  # Debugging
            print( f"Traversing collisions..." )  # Debugging

            numEntries = self.pickerQueue.getNumEntries()
            print( f"Number of collision entries: { numEntries }" )  # Debugging

            if numEntries > 0:
                # Sort entries so the closest is first
                self.pickerQueue.sortEntries()
                entry = self.pickerQueue.getEntry( 0 )
                point = entry.getSurfacePoint( self.render )

                print( f"Collision detected at: { point }" )  # Debugging
                picked_obj = entry.getIntoNodePath()
                print( f"Clicked node ID or name: { picked_obj.getName() }" )
                # Update the terrain center to the clicked point
                self.trCamera.terrainCenter = point
                self.trCamera.updateCameraPosition()
            else:
                print( "No collisions detected." )  # Debugging

app = MyApp()
app.run()
