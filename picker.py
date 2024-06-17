from panda3d.core import BitMask32, CollisionHandlerQueue, CollisionNode, CollisionRay, CollisionTraverser


class Picker:
    def __init__(self, camera ):
        self.camera = camera
        self.pickerQueue = None
        self.picker = None
        self.pickerRay = None
        self.pickerNP = None
        self.pickerNode = None
        self.createPicker()

    def createPicker( self ):
        self.picker = CollisionTraverser()
        self.pickerQueue = CollisionHandlerQueue()
        self.pickerNode = CollisionNode( 'mouseRay' )
        self.pickerNP = self.camera.attachNewNode( self.pickerNode )
        self.pickerNode.setFromCollideMask( BitMask32.bit( 1 ) )
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid( self.pickerRay )
        self.picker.addCollider( self.pickerNP, self.pickerQueue )
        return self.picker