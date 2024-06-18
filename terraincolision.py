from panda3d.core import BitMask32, CollisionNode, CollisionPolygon, GeoMipTerrain, GeomNode, GeomTriangles, \
    GeomVertexReader

from customcollisionpolygon import CustomCollisionPolygon


class TerrainCollision:
    def __init__( self, terrain: GeoMipTerrain ):
        self.terrain = terrain

    def createTerrainCollision( self ):
        root = self.terrain.getRoot()
        # Iterate over each GeomNode
        for child in root.getChildren():
            if isinstance( child.node(), GeomNode ):
                customCollisionPolygon = CustomCollisionPolygon( child )
                if customCollisionPolygon.getAngle < 0.2:
                    customCollisionPolygon.attachToTerrainChildNode()
