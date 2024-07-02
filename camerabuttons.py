from direct.gui.DirectButton import DirectButton

from camera import TerrainCamera


class CameraButtons:
    def __init__( self, terrainCamera: TerrainCamera ):
        self.camera = terrainCamera
        self.create_above_button()
        self.create_rotate_left_button()
        self.create_rotate_right_button()
        self.create_distance_view_button()

    def create_rotate_left_button( self ):
        rotate_button = DirectButton(
            text = "Rotate Left",
            command = self.camera.rotateCamera,
            pos = (0, 0, -0.9),
            text_scale = 0.5,
            scale = 0.1
        )

    def create_rotate_right_button( self ):
        rotate_button = DirectButton(
            text = "Rotate Right",
            command = self.camera.rotateCamera,
            pos = ( 0, 0, 0.9 ),
            scale = 0.1,
            text_scale = 0.5,
            extraArgs = [ -1 ]
        )

    def create_above_button( self ) :
        rotate_button = DirectButton(
            text = "Hover Above",
            command = self.camera.hoverAbove,
            pos = ( 0.9, 0.9, 0 ),
            scale = 0.1,
            text_scale = 0.5,
        )

    def create_distance_view_button( self ):
        rotate_button = DirectButton(
            text = "Distance View",
            command = self.camera.hoverDistance,
            pos = ( -0.9, -0.9, 0 ),
            text_scale = 0.5,
            scale = 0.1
        )
