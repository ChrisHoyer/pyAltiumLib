from pyaltiumlib.pcblib.records.base import _GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader, Coordinate, CoordinatePoint
from pyaltiumlib.datatypes import PCBTextJustification, PCBTextKind

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
            self.stroke_width = Coordinate.parse_bin( block.read(4) ) 
            
            if block.length() >= 123:
                
                block.read_int16() # Unknown
                block.read_byte() # Unknown
                
                self.text_kind = PCBTextKind( block.read_int8() )
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
           
        self.alignment = {
            "vertical": self.font_inverted_rect_justification.get_vertical(),
            "horizontal": self.font_inverted_rect_justification.get_horizontal(),
            "rotation": -self.rotation,
            "anchor": self.corner1.copy()
            }
                
        # bounding box
        left_top = self.corner1.copy()
        right_bot = self.corner1.copy()
        left_top.y = left_top.y - self.font_inverted_rect_height
        right_bot.x = right_bot.x + self.font_inverted_rect_width
        
        # Set anchor point
        if self.alignment["vertical"] == "text-after-edge":
            self.alignment["anchor"].y = self.corner1.y - self.font_inverted_rect_height
            left_top.y = left_top.y - self.font_inverted_rect_height
            right_bot.y = right_bot.y - self.font_inverted_rect_height
            
        elif self.alignment["vertical"] == "central":
            self.alignment["anchor"].y = self.corner1.y - self.font_inverted_rect_height/2
            
        elif self.alignment["vertical"] == "text-before-edge":
            self.alignment["anchor"].y = self.corner1.y
            left_top.y = left_top.y + self.font_inverted_rect_height
            right_bot.y = right_bot.y + self.font_inverted_rect_height
            
        if self.alignment["horizontal"] == "end":
            self.alignment["anchor"].x = self.corner1.x + self.font_inverted_rect_width
        elif self.alignment["horizontal"] == "middle":
            self.alignment["anchor"].x = self.corner1.x + self.font_inverted_rect_width/2
        elif self.alignment["horizontal"] == "start":
            self.alignment["anchor"].x = self.corner1.x
            
        # rotate
        self.alignment["anchor"] = self.alignment["anchor"].rotate(self.corner1, -self.rotation)
        left_top = left_top.rotate(self.corner1, -self.rotation)
        right_bot = right_bot.rotate(self.corner1, -self.rotation)                 

        return [left_top, right_bot]
    
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
        
        insert = (self.alignment["anchor"] * zoom) + offset
        layer = self.get_layer_by_id(self.layer)
        
        if  self.text_kind == PCBTextKind(0):
            font =  self.text_kind.get_font()
        else:
            font =  self.font_name
        
        drawing_primitive = dwg.text(self.text,
                                     font_size = int(self.height * zoom),
                                     font_family = font, 
                                     insert = insert.to_int_tuple(),
                                     fill = layer.color.to_hex(),
                                     dominant_baseline=self.alignment["vertical"],
                                     text_anchor=self.alignment["horizontal"],
                                     transform=f"rotate({self.alignment['rotation']} {int(insert.x)} {int(insert.y)})"
                                     )                

        self.Footprint.drawing_layer[self.layer].add( drawing_primitive )