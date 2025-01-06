from PIL import ImageFont

from pyaltiumlib.schlib.records.base import _SchCommonParam
from pyaltiumlib.datatypes import (
     SchematicLineWidth, SchematicPinSymbol, SchematicPinElectricalType
    )

class SchPin(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 2 ):
            raise TypeError("Incorrect assigned schematic record")
        
        
        self.symbol_inneredge = SchematicPinSymbol(self.rawdata.get('symbol_inneredge', 0))
        self.symbol_outeredge = SchematicPinSymbol(self.rawdata.get('symbol_outeredge', 0))
        self.symbol_inside = SchematicPinSymbol(self.rawdata.get('symbol_inside', 0))
        self.symbol_outside = SchematicPinSymbol(self.rawdata.get('symbol_outside', 0))   
        self.symbol_linewidth = SchematicLineWidth(self.rawdata.get('symbol_linewidth', 0))
        
        self.description = self.rawdata.get('description', 0)
        self.name = self.rawdata.get('name', 0) 
        self.designator = self.rawdata.get('designator', 0)
        
        self.electrical_type = SchematicPinElectricalType(self.rawdata.get('electrical_type', 0))  
        
        self.rotated = self.rawdata.get('rotated', 0)
        self.flipped = self.rawdata.get('flipped', 0)
        self.hide = self.rawdata.get('hide', 0)
        self.show_name = self.rawdata.get('show_name', 0)
        self.show_designator = self.rawdata.get('show_designator', 0) 
        
        self.graphically_locked = self.rawdata.get('graphically_locked', 0) 
        
        self.pinlength = self.rawdata.get('length', 0)
        
        
    def __repr__(self):
        return f"SchPin"
        
# =============================================================================
#     Drawing related
# =============================================================================   
         
    def get_bounding_box(self):
        """
        Return bounding box
        """

        self.end = self.location.copy()
                
        if self.rotated and self.flipped:
            self.end.y = self.end.y + self.pinlength
            
        if self.rotated and not self.flipped:
            self.end.y = self.end.y - self.pinlength
            
        if not self.rotated and self.flipped:
            self.end.x = self.end.x - self.pinlength
            
        if not self.rotated and not self.flipped:
            self.end.x = self.end.x + self.pinlength
 
        # print("SchPin - BoundingBox")
        # print(f"Start: {self.location}")
        # print(f"End: {self.end}")
         
        return [self.location, self.end]

    
    def draw(self, graphic, offset, zoom):
        """
        Draw Element using ImageDraw Module of Pillow with support for zoom and offsetting.
        """

        loc_x = float( (self.location.x * zoom) + offset.x )
        loc_y = float( (self.location.y * zoom) + offset.y )
        corner_x = float( (self.end.x * zoom) + offset.x )
        corner_y = float( (self.end.y * zoom) + offset.y )
        
        font = ImageFont.truetype("arial.ttf", size=12)
        graphic.text( (corner_x, corner_y), self.name, font=font, 
                     fill=self.color.to_hex(), align="left")
        
        graphic.line(
            [loc_x, loc_y, corner_x, corner_y],
            fill=self.color.to_hex(),
            width=4,
        )

        
        
        
    



