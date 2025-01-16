from pyaltiumlib.pcblib.records.base import _GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader, Coordinate, CoordinatePoint
from pyaltiumlib.datatypes import PCBPadShape

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
        

        first_block = BinaryReader.from_stream( stream )
        second_block = BinaryReader.from_stream( stream )

        # Read First Block 
        if first_block.has_content():
            self.read_common( first_block.read(13) )
            self.location = first_block.read_bin_coord()
            
            self.size_top = first_block.read_bin_coord()
            self.size_middle = first_block.read_bin_coord()
            self.size_bottom = first_block.read_bin_coord()
            self.hole_size = first_block.read_int32()
            
            self.shape_top = PCBPadShape( first_block.read_int8() )
            self.shape_middle = PCBPadShape( first_block.read_int8() )
            self.shape_bottom = PCBPadShape( first_block.read_int8() )
            
            self.rotation = first_block.read_double() 
            self.is_plated = bool( first_block.read_int8() )
            
            first_block.read_byte() # Unknown
            
            self.stack_mode = first_block.read_int8()
            
            first_block.read( 22 ) # Unknown 
            
            self.expansion_paste_mask = Coordinate.parse_bin(first_block.read(4))
            self.expansion_solder_mask = Coordinate.parse_bin(first_block.read(4))      
    
            first_block.read( 7 ) # Unknown 
    
            self.expansion_manual_paste_mask = first_block.read_int8(signed=True)
            self.expansion_manual_solder_mask = first_block.read_int8(signed=True)   
    
            first_block.read( 7 ) # Unknown 
            
            self.jumperid = first_block.read_int16()
        
        
        # Read Second Block
        if second_block.has_content():
            
            print("Second Block has content!")
            pad_x_size = [ Coordinate.parse_bin(second_block.read(4)) for x in range(29) ]
            pad_y_size = [ Coordinate.parse_bin(second_block.read(4)) for x in range(29) ]
            
            self.size_middle_layers = [ CoordinatePoint(pad_x_size[i], pad_y_size[i]) for i in range(29)]
        
# =============================================================================
#     Drawing related
# ============================================================================= 


    def get_bounding_box(self):
        """
        Return bounding box for the object
        """
        
        size_x = min(float(self.size_top.x), float(self.size_middle.x), float(self.size_bottom.x))
        size_y = min(float(self.size_top.y), float(self.size_middle.y), float(self.size_bottom.y)) 

        corners = [
            CoordinatePoint(self.location.x - size_x / 2, self.location.y - size_y / 2),
            CoordinatePoint(self.location.x + size_x / 2, self.location.y - size_y / 2),
            CoordinatePoint(self.location.x + size_x / 2, self.location.y + size_y / 2),
            CoordinatePoint(self.location.x - size_x / 2, self.location.y + size_y / 2),
        ]
        
        rotated_corners = [corner.rotate(self.location, self.rotation) for corner in corners]

        xs = [corner.x for corner in rotated_corners]
        ys = [corner.y for corner in rotated_corners]

        min_x, min_y = min(xs), min(ys)
        max_x, max_y = max(xs), max(ys)
        
        return [CoordinatePoint(Coordinate(min_x), Coordinate(min_y)),
                CoordinatePoint(Coordinate(max_x), Coordinate(max_y))]

    
    def draw_svg(self, dwg, offset, zoom):
        """
        Draw element using svgwrite
        Args:
            dwg: svg Drawing
            offset (int): SchematicCoordinate with drawing center point
            zoom (float): Scaling Factor for all elements
        Returns:
            None
        """
        
        center = (self.location.copy() * zoom) + offset
        start = ((self.location.copy() - (self.size_top * 0.5)) * zoom) + offset
        end = ((self.location.copy() + (self.size_top * 0.5)) * zoom) + offset
        
        layer_cu = self.get_layer_by_id(self.layer)
        
        # start is lower left corner -> needs to be upper right
        size = start - end
        start.y = start.y - size.y
        
        
        
        print(f"Shape: {self.shape_top} - {self.shape_middle} - {self.shape_bottom}")
        print(f"Designator: {self.designator}")

        
        dwg.add(dwg.rect(insert = start.get_int(),
                         size = [ abs(x) for x in size.get_int() ],
                         fill = layer_cu.color.to_hex(),
                         transform=f"rotate(-{self.rotation} {center.x} {center.y})"
                         ))
        
        dwg.add(dwg.text(self.designator,
                         insert = center.get_int(),
                         fill = "white",
                         dominant_baseline="central", text_anchor="middle",
                         transform=f"rotate(-{self.rotation} {center.x} {center.y})"
                         ))