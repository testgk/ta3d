from panda3d.core import BitMask32, CollisionNode, CollisionPolygon, GeoMipTerrain, GeomNode, GeomVertexReader


class TerrainCollision:
    def __init__( self, terrain: GeoMipTerrain ):
        self.terrain = terrain

    def createTerrainCollision( self ):
        root = self.terrain.getRoot()
        # Iterate over each GeomNode
        for child in root.getChildren():
            if isinstance( child.node(), GeomNode ):
                geom_node = child.node()
                geom = geom_node.getGeom( 0 )  # Assuming each GeomNode has one Geom
                vertex_data = geom.getVertexData()

                tris = geom.getPrimitive( 0 )  # Assuming the first primitive is triangles
                tris = tris.decompose()

                collision_node = CollisionNode( f'terrain_{ child.getName() }')
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

                    poly = CollisionPolygon( vertices[0],  vertices[1],  vertices[2] )
                    collision_node.addSolid(poly)

                collision_node_path = child.attachNewNode( collision_node )
                collision_node_path.show()  # Show the collision node for debugging
                print( f"Collision node { child.getName() } created and attached to terrain")  # Debugging
