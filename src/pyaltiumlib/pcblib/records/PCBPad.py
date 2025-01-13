from pyaltiumlib.pcblib.records.base import _GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader

class PcbPad(_GenericPCBRecord):
    
    def __init__(self, parent, stream):
        
        super().__init__(parent)
        
        self.parse( stream )
    
        
    def __repr__(self):
        return f"PCBPad"
    
    
    def parse(self, stream):
        
        self.designator = BinaryReader.from_stream( stream ).read_string_block()
        
        # Unknown
        BinaryReader.from_stream( stream )
        BinaryReader.from_stream( stream ).read_string_block()
        BinaryReader.from_stream( stream )  
        
        # Read First Block
        first_block = BinaryReader.from_stream( stream )
        
        self.read_common( first_block.read(13) )
        self.location = first_block.read_coordinatepoint()
        self.size_top = first_block.read_coordinatepoint()
        self.size_middle = first_block.read_bin_coord()
        self.size_bottom = first_block.read_bin_coord()
        self.hole_size = first_block.read_int32()
        self.shape_top = first_block.read_byte()
        
        
        second_block = BinaryReader.from_stream( stream )        
        
        
