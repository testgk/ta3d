from panda3d.core import AmbientLight, PointLight

from camera import TerrainCamera
from camerabuttons import CameraButtons
from terraincolision import TerrainCollision
from direct.showbase.ShowBase import ShowBase
from maps.terrainprovider import TerrainProvider


class MyApp(ShowBase):
    def __init__( self ):
        ShowBase.__init__( self )
        terrainProvider = TerrainProvider( self.loader )
        self.terrainInfo = terrainProvider.create_terrain( "heightmap1" )
        self.terrain = self.terrainInfo.terrain

        self.terrain.getRoot().reparentTo( self.render )
        self.terrain.setFocalPoint( self.camera )
        self.disableMouse()
        self.terrainCamera = TerrainCamera( self.camera, self.mouseWatcherNode, self.camNode, self.render, self.terrainInfo.terrainCenter )
        self.cameraButtons = CameraButtons( self.terrainCamera )
        self.terrainCollision = TerrainCollision( self.terrain )
        self.terrainCollision.createTerrainCollision()
        self.accept( 'mouse1', self.on_map_click )
        # Start a task to update the camera position
        self.taskMgr.add( self.terrainCamera.update_camera_task, "UpdateCameraTask" )

        # Add a point light
        plight = PointLight( "plight" )
        plight_node = self.render.attachNewNode(plight)
        plight_node.setPos( 60, 60, 15 )
        self.render.setLight( plight_node )

        # Add an ambient light
        alight = AmbientLight("alight")
        alight.setColor( ( 0.5, 0.5, 0.7, 1 ) )
        alight_node = self.render.attachNewNode(alight)
        self.render.setLight(alight_node)

    def on_map_click( self ):
        self.terrainCamera.on_map_click()

app = MyApp()
app.run()
