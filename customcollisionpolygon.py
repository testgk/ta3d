import math

from panda3d.core import BitMask32, CollisionNode, CollisionPolygon, GeomNode, GeomVertexReader, NodePath, Vec3


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
        for prIndex in range( primStart, primEnd ):
            vi = tris.getVertex(prIndex)
            vertex_reader.setRow(vi)
            v = vertex_reader.getData3()
            vertices.append( v )
        all_vertices.append( vertices )
    return all_vertices


def calculate_angle( normal_vector, reference_plane_normal = Vec3( 0, 0, 1 ) ):
    # Calculate the angle between the normal vector and the reference plane normal
    dot_product = normal_vector.dot( reference_plane_normal )
    magnitude_product = normal_vector.length() * reference_plane_normal.length()
    angle_radians = math.acos(dot_product / magnitude_product)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees


class CustomCollisionPolygon:
    def __init__( self, child: NodePath ):
        self.__collision_node_path = None
        self.__collision_node = None
        self._child = child
        geom_node = self._child.node()
        geom = geom_node.getGeom( 0 )  # Assuming each GeomNode has one Geom
        self.__vertices = getVertices( geom )
        self.__collision_node = CollisionNode( f'terrain_{ self._child.getName()}' )
        self.__collision_node.setIntoCollideMask( BitMask32.bit( 1 ) )
        for vertex in self.__vertices:
            self.__poly = CollisionPolygon( vertex[ 0 ], vertex[ 1 ], vertex[ 2 ] )
            # Compute two edges of the polygon
            edge1 = vertex[ 1 ] - vertex[ 0 ]
            edge2 = vertex[ 2 ] - vertex[ 0 ]
            normal = edge1.cross( edge2 ).normalized()
            self.__angle = calculate_angle( normal )
            print( f"{self._child.getName() } angle = {self.__angle}")
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

    @property
    def getAngle( self ):
        return self.__angle

    def attachToTerrainChildNode( self ):
        self.__collision_node_path = self._child.attachNewNode( self.__collision_node )
        self.__collision_node_path.show()  # Show the collision node for debugging
        print( f"Collision node { self._child.getName() } created and attached to terrain" )  # Debugging

