from pyaltiumlib.pcblib.records.base import _GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader, Coordinate, CoordinatePoint

class PcbComponentBody(_GenericPCBRecord):
    
    def __init__(self, parent, stream):
        
        super().__init__(parent)
        
        self.parse( stream )
    
        
    def __repr__(self):
        return f"PCBComponentBody"
    
    
    def parse(self, stream):
        
        block = BinaryReader.from_stream( stream )
        string = BinaryReader.from_stream( stream )
        
        
# =============================================================================
#     Drawing related
# ============================================================================= 