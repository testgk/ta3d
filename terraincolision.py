from panda3d.core import GeoMipTerrain, GeomNode

from customcollisionpolygon import CustomCollisionPolygon

polygons = {}

class TerrainCollision:
    def __init__( self, terrain: GeoMipTerrain ):
        self.terrain = terrain

    def createTerrainCollision( self ):
        root = self.terrain.getRoot()
        # Iterate over each GeomNode
        for child in root.getChildren():
            if isinstance( child.node(), GeomNode ):
                customCollisionPolygon = CustomCollisionPolygon( child )
                if True or customCollisionPolygon.getAngle < 0.2:
                    customCollisionPolygon.attachToTerrainChildNode()
                    polygons[ child.getName() ] = customCollisionPolygon
