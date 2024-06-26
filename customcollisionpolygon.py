import math

from panda3d.core import BitMask32, CollisionNode, CollisionPolygon, GeomNode, GeomVertexReader, NodePath, Vec3


def getPolygon( row, column ) -> 'CustomCollisionPolygon':
    return polygons[ f"gmm{row}x{column}" ]


def getPolygonByName( name: str ) -> 'CustomCollisionPolygon':
    return polygons[ name ]


def addPolygon( name, polygon ):
    polygons[ name ] = polygon


def getVertices( geom: GeomNode ) -> list:
    all_vertices = [ ]
    tris = geom.getPrimitive( 0 )  # Assuming the first primitive is triangles
    tris = tris.decompose()
    vertex_data = geom.getVertexData()
    vertex_reader = GeomVertexReader( vertex_data, 'vertex' )

    for i in range( tris.getNumPrimitives() ):
        primStart = tris.getPrimitiveStart( i )
        primEnd = tris.getPrimitiveEnd( i )
        assert primEnd - primStart == 3

        vertices = [ ]
        for prIndex in range( primStart, primEnd ):
            vi = tris.getVertex( prIndex )
            vertex_reader.setRow( vi )
            v = vertex_reader.getData3()
            vertices.append( v )
        all_vertices.append( vertices )
    return all_vertices


polygons = { }


def calculate_angle( normal_vector, reference_plane_normal = Vec3( 0, 0, 1 ) ):
    # Calculate the angle between the normal vector and the reference plane normal
    dot_product = normal_vector.dot( reference_plane_normal )
    magnitude_product = normal_vector.length() * reference_plane_normal.length()
    angle_radians = math.acos( dot_product / magnitude_product )
    angle_degrees = math.degrees( angle_radians )
    return angle_degrees


def triangle_area( v0, v1, v2 ):
    # Use the cross product to get the area of the triangle
    edge1 = v1 - v0
    edge2 = v2 - v0
    cross_product = edge1.cross( edge2 )
    area = 0.5 * cross_product.length()
    return area


class CustomCollisionPolygon:
    def __init__( self, child: NodePath, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.__collision_node_path = None
        self.__collision_node = None
        self._child = child
        geom_node = self._child.node()
        geom = geom_node.getGeom( 0 )  # Assuming each GeomNode has one Geom
        self.__vertices = getVertices( geom )
        self.__collision_node = CollisionNode( f'terrain_{self._child.getName()}' )
        self.__collision_node.setIntoCollideMask( BitMask32.bit( 1 ) )
        triangleCount = 0
        for vertex in self.__vertices:
            self.__poly = CollisionPolygon( vertex[ 0 ], vertex[ 1 ], vertex[ 2 ] )
            # Compute two edges of the polygon
            edge1 = vertex[ 1 ] - vertex[ 0 ]
            edge2 = vertex[ 2 ] - vertex[ 0 ]
            normal = edge1.cross( edge2 ).normalized()
            self.__name = self._child.getName()
            self.__angle = calculate_angle( normal )
            self.__area = triangle_area( vertex[ 0 ], vertex[ 1 ], vertex[ 2 ] )
            pos = self.__name[ 3: ].split( 'x' )
            self.__row = int( pos[ 0 ] )
            self.__col = int( pos[ 1 ] )
            print(
                f"{ self.__name }: triangle: { triangleCount++ } { self.__angle }, row = { self.__row }, column = { self.__col } area = { self.__area }" )
            self.__collision_node.addSolid( self.__poly )
            self.__collision_node.setPythonTag( 'custom_collision_polygon', self )
            addPolygon( self.__name, self )

    @property
    def vertices( self ) -> list[ GeomVertexReader ]:
        return self.__vertices

    @property
    def name( self ) -> str:
        return self.__name

    @property
    def collisionPolygon( self ) -> GeomNode:
        return self.__poly

    @property
    def collisionNodePath( self ) -> NodePath:
        return self.__collision_node_path

    @property
    def getNeighbor( self ) -> 'CustomCollisionPolygon':
        try:
            return getPolygon( self.__row + 1, self.__col )
        except:
            print( 'no neighbor' )

    @property
    def getAngle( self ):
        return self.__angle

    def __str__( self ):
        return f'{ self.__name }, row: { self.__row }, column: { self.__col }, area: { self.__area }, angle: { self.__angle }'

    def attachToTerrainChildNode( self ):
        self.__collision_node_path = self._child.attachNewNode( self.__collision_node )
        self.__collision_node_path.show()  # Show the collision node for debugging
        print( f"Collision node {self.__name} created and attached to terrain" )  # Debugging
