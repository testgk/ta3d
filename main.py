from lights import Lights
from camera import TerrainCamera
from camerabuttons import CameraButtons
from terraincolision import TerrainCollision
from direct.showbase.ShowBase import ShowBase
from maps.terrainprovider import TerrainProvider


class MyApp( ShowBase ):
    def __init__( self ):
        ShowBase.__init__( self )
        terrainProvider = TerrainProvider( self.loader )
        self.terrainInfo = terrainProvider.create_terrain( "heightmap1" )
        self.terrain = self.terrainInfo.terrain

        self.terrain.getRoot().reparentTo( self.render )
        self.terrain.setFocalPoint( self.camera )
        self.disableMouse()
        self.terrainCamera = TerrainCamera( self.camera,
                                            self.mouseWatcherNode,
                                            self.camNode,
                                            self.render,
                                            self.terrainInfo.terrainCenter )
        self.cameraButtons = CameraButtons( self.terrainCamera )
        self.lights = Lights( self.render )
        self.terrainCollision = TerrainCollision( self.terrain )
        self.terrainCollision.createTerrainCollision()
        self.accept( 'mouse1', self.on_map_click )
        # Start a task to update the camera position
        self.taskMgr.add( self.terrainCamera.updateCameraTask, "UpdateCameraTask" )

    def on_map_click( self ):
        self.terrainCamera.on_map_click()


app = MyApp()
app.run()
