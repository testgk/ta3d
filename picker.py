from panda3d.core import BitMask32, CollisionHandlerQueue, CollisionNode, CollisionRay, CollisionTraverser


class Picker:
    def __init__(self, camera ):
        self.__camera = camera
        self.__picker = CollisionTraverser()
        self.__pickerQueue = CollisionHandlerQueue()
        self.__pickerNode = CollisionNode( 'mouseRay' )
        self.__pickerNP = self.__camera.attachNewNode( self.__pickerNode )
        self.__pickerNode.setFromCollideMask( BitMask32.bit( 1 ) )
        self.__pickerRay = CollisionRay()
        self.__pickerNode.addSolid( self.__pickerRay )
        self.__picker.addCollider( self.__pickerNP, self.__pickerQueue )

    @property
    def picker( self ):
        return self.__picker

    @property
    def pickerQueue( self ):
        return self.__pickerQueue

    @property
    def pickerRay( self ):
        return self.__pickerRay
