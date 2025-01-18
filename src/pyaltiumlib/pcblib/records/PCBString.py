from pyaltiumlib.pcblib.records.base import _GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader, Coordinate, CoordinatePoint
from pyaltiumlib.datatypes import PCBTextJustification

class PcbString(_GenericPCBRecord):
    
    def __init__(self, parent, stream):
        
        super().__init__(parent)
        
        self.parse( stream )
    
        
    def __repr__(self):
        variables = ', '.join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}({variables})"
    
    
    def parse(self, stream):
        
        block = BinaryReader.from_stream( stream )
        string = BinaryReader.from_stream( stream )

        # Read Block 
        if block.has_content():
            self.read_common( block.read(13) )
            self.corner1 = block.read_bin_coord()
            self.height = Coordinate.parse_bin( block.read(4) ) 
            self.stroke_font = block.read_int16()
            self.rotation = block.read_double()
            self.mirrored = bool(block.read_byte())
            self.stroke_width = block.read_int32()
            
            if block.length() >= 123:
                
                block.read_int16() # Unknown
                block.read_byte() # Unknown
                
                self.text_kind = block.read_byte()
                self.font_bold = block.read_byte()
                self.font_italic = block.read_byte()
                self.font_name = block.read_unicode_text()
                self.barcode_margin_lr = block.read_int32()
                self.barcode_margin_tb = block.read_int32()                
                
                block.read_int32() # Unknown
                block.read_int32() # Unknown
                block.read_byte() # Unknown
                block.read_byte() # Unknown
                block.read_int32() # Unknown
                block.read_int16() # Unknown
                block.read_int32() # Unknown
                block.read_int32() # Unknown  
                
                self.font_inverted = block.read_byte()
                self.font_inverted_border = block.read_int32()
                self.widestring_index = block.read_int32()
                
                block.read_int32() # Unknown
                
                self.font_inverted_rect = block.read_byte()
                self.font_inverted_rect_width = Coordinate.parse_bin(block.read(4))
                self.font_inverted_rect_height = Coordinate.parse_bin(block.read(4))
                self.font_inverted_rect_justification = PCBTextJustification( block.read_int8() )              
                self.font_inverted_rect_text_offset = block.read_int32() 
                
                
        if string.has_content():
            self.text = string.read_string_block()
            
            
# =============================================================================
#     Drawing related
# =============================================================================

    def get_bounding_box(self):
        """
        Return bounding box for the object
        """
        
        print()
        print( self )
        print()
        
        self.alignment = {
            "vertical": self.font_inverted_rect_justification.get_vertical(),
            "horizontal": self.font_inverted_rect_justification.get_horizontal(),
            "rotation": - self.rotation,
            "position" : self.corner1.copy()
            }
        
        self.corner2 = self.corner1.copy()
        self.corner2.x = len(self.text) * self.height * 0.6
        self.corner2.y = self.corner2.y + self.height

        return [self.corner1, self.corner2]
    
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
        
        insert = (self.corner1 * zoom) + offset
        layer = self.get_layer_by_id(self.layer)
        
        drawing_primitive = dwg.text(self.text,
                                     font_size = int(self.height * zoom),
                                     font_family = self.font_name, 
                                     insert = insert.to_int_tuple(),
                                     fill = layer.color.to_hex(),
                                     dominant_baseline=self.alignment["vertical"],
                                     text_anchor=self.alignment["horizontal"],
                                     transform=f"rotate({self.alignment['rotation']} {int(insert.x)} {int(insert.y)})"
                                     )                
        
        self.Footprint.drawing_layer[self.layer].add( drawing_primitive )