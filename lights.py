from panda3d.core import AmbientLight, PointLight


class Lights:
    def __init__(self, render ):
        self.render = render

    def lightsOn(self):
        # Add a point light
        plight = PointLight( "plight" )
        plight_node = self.render.attachNewNode(plight)
        plight_node.setPos( 60, 60, 15 )
        self.render.setLight( plight_node )

        # Add an ambient light
        alight = AmbientLight( "alight" )
        alight.setColor( ( 0.5, 0.5, 0.7, 1 ) )
        alight_node = self.render.attachNewNode( alight )
        self.render.setLight( alight_node )