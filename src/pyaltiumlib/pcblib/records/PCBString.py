from pyaltiumlib.pcblib.records.base import _GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader, Coordinate, CoordinatePoint

class PcbString(_GenericPCBRecord):
    
    def __init__(self, parent, stream):
        
        super().__init__(parent)
        
        self.parse( stream )
    
        
    def __repr__(self):
        return f"PcbString"
    
    
    def parse(self, stream):
        
        block = BinaryReader.from_stream( stream )
        string = BinaryReader.from_stream( stream )

        # Read Block 
        if block.has_content():
            self.read_common( block.read(13) )
            self.corner = block.read_bin_coord()
            self.height = Coordinate.parse_bin( block.read(4) ) 
        
# =============================================================================
#     Drawing related
# ============================================================================= 