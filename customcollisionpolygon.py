from panda3d.core import BitMask32, CollisionNode, CollisionPolygon, GeomNode, GeomVertexReader, NodePath


def getVertices( geom: GeomNode ) -> list:
    all_vertices = []
    tris = geom.getPrimitive(0)  # Assuming the first primitive is triangles
    tris = tris.decompose()
    vertex_data = geom.getVertexData()
    vertex_reader = GeomVertexReader(vertex_data, 'vertex')

    for i in range(tris.getNumPrimitives()):
        primStart = tris.getPrimitiveStart(i)
        primEnd = tris.getPrimitiveEnd(i)
        assert primEnd - primStart == 3

        vertices = []
        for prIndex in range(primStart, primEnd):
            vi = tris.getVertex(prIndex)
            vertex_reader.setRow(vi)
            v = vertex_reader.getData3()
            vertices.append(v)
        all_vertices.append( vertices )
    return all_vertices


class CustomCollisionPolygon:
    def __init__( self, child: NodePath ):
        self.__collision_node_path = None
        self.__collision_node = None
        self._child = child
        geom_node = self._child.node()
        geom = geom_node.getGeom( 0 )  # Assuming each GeomNode has one Geom
        self.__collision_node = CollisionNode( f'terrain_{ self._child.getName()}' )
        self.__collision_node.setIntoCollideMask( BitMask32.bit( 1 ) )
        self.__vertices = getVertices( geom )
        for vertex in self.__vertices:
            self.__poly = CollisionPolygon( vertex[ 0 ], vertex[ 1 ], vertex[ 2 ] )
            self.__collision_node.addSolid( self.__poly )

    @property
    def vertices(self) -> list[ GeomVertexReader ]:
        return self.__vertices

    @property
    def collisionPolygon(self) -> GeomNode:
        return self.__poly

    @property
    def collisionNodePath(self) -> NodePath:
        return self.__collision_node_path

    def attachToTerrainChildNode( self ):
        self.__collision_node_path = self._child.attachNewNode( self.__collision_node )
        self.__collision_node_path.show()  # Show the collision node for debugging
        print( f"Collision node { self._child.getName() } created and attached to terrain" )  # Debugging
