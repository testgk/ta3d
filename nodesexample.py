from panda3d.core import GeoMipTerrain, GeomNode, GeomVertexReader, NodePath, BitMask32, LVector3
from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles, Geom

def getVertices(geom: GeomNode ) -> list:
    all_vertices = []
    tris = geom.getPrimitive(0)  # Assuming the first primitive is triangles
    tris = tris.decompose()
    vertex_data = geom.getVertexData()
    vertex_reader = GeomVertexReader(vertex_data, 'vertex')

    for i in range(tris.getNumPrimitives()):
        primStart = tris.getPrimitiveStart(i)
        primEnd = primStart + 3
        vertices = []
        for prIndex in range(primStart, primEnd):
            vi = tris.getVertex(prIndex)
            vertex_reader.setRow(vi)
            v = vertex_reader.getData3()
            vertices.append(v)
        all_vertices.append(vertices)
    return all_vertices

def create_polygon(vertices, name="polygon"):
    # Create a GeomVertexData object to hold the vertices
    vertex_format = GeomVertexFormat.get_v3()
    vertex_data = GeomVertexData(name, vertex_format, Geom.UHStatic)

    # Create writers to add data to the vertex data
    vertex_writer = GeomVertexWriter(vertex_data, 'vertex')

    # Add the vertices to the vertex data
    for vertex in vertices:
        vertex_writer.addData3f(vertex)

    # Create the GeomPrimitive object to hold the triangles
    triangles = GeomTriangles(Geom.UHStatic)
    for i in range(1, len(vertices) - 1):
        triangles.addVertices(0, i, i + 1)

    # Create a Geom object to hold the vertex data and triangles
    geom = Geom(vertex_data)
    geom.addPrimitive(triangles)

    # Create a GeomNode to hold the Geom object
    geom_node = GeomNode(name)
    geom_node.addGeom(geom)

    return geom_node

def display_polygon(parent: NodePath, vertices, name="polygon"):
    geom_node = create_polygon(vertices, name)
    geom_node_path = parent.attachNewNode(geom_node)
    geom_node_path.setRenderModeWireframe()  # Optional: display as wireframe for clarity
    geom_node_path.setTwoSided(True)  # Optional: make polygon two-sided for visibility

    return geom_node_path

def createTerrainCollision( terrain: GeoMipTerrain ):
    root = terrain.getRoot()

    # Iterate over each GeomNode
    for child in root.getChildren():
        if isinstance(child.node(), GeomNode):
            geom_node = child.node()
            all_triangles = getVertices( geom_node.getGeom(0) )
            for i, vertices in enumerate(all_triangles):
                display_polygon(child, vertices, f"polygon_{ child.getName()}_{ i }" )

# Example usage
terrain = GeoMipTerrain("terrain")
terrain.setHeightfield("heightmap.png")
terrain.setBlockSize(32)  # Example block size in meters
terrain.generate()
terrain.getRoot().reparentTo(render)

# Create the collision for the terrain
createTerrainCollision(terrain)
