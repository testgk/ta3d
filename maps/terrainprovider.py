from panda3d.core import Filename, GeoMipTerrain, PNMImage, Point3


class TerrainInfo:
    def __init__( self, terrain: GeoMipTerrain, heightMap: PNMImage ):
        self.terrain = terrain
        self.heightMap = heightMap
        terrain_size = heightMap.getXSize()
        self.terrainCenter = Point3( terrain_size / 2, terrain_size / 2, 0 )
        self.terrainSize = heightMap.getXSize()


class TerrainProvider:
    def __init__( self, loader ):
        self._loader = loader

    def create_terrain(self, terrainName: str ) -> TerrainInfo:
        terrain = GeoMipTerrain( "terrain" )
        heightmap = PNMImage( Filename( f"maps/{ terrainName }.png" ) )
        terrain.setHeightfield( heightmap )
        # Set terrain properties
        terrain.setBlockSize( 32 )
        terrain.setNear( 40 )
        terrain.setFar( 200 )
        terrain.getRoot().setSz( 100 )
        # Calculate the center of the terrain
        terrain.generate()
        texture = self._loader.loadTexture( "maps/terrain_texture.png" )
        terrain.getRoot().setTexture( texture )
        return TerrainInfo( terrain, heightmap )
