import math
from pyaltiumlib.schlib.records.base import _SchCommonParam
from pyaltiumlib.datatypes import SchCoord, SchematicLineWidth


class SchArc(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 12 ):
            raise TypeError("Incorrect assigned schematic record")
            
        self.radius = SchCoord.parse_dpx("radius", self.rawdata)
        
        self.angle_start = float( self.rawdata.get('startangle', 0) )            
        self.angle_end = float( self.rawdata.get('endangle', 0) )             
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0)) 
        
    def __repr__(self):
        return f"SchArc "        
        
# =============================================================================
#     Drawing related
# ============================================================================= 
    def get_bounding_box(self, InvertY=False):
        """
        Return bounding box
        """

        start_x = self.location.x - self.radius
        start_y = self.location.y - self.radius        
        end_x = self.location.x + self.radius
        end_y = self.location.y + self.radius

        min_x = min(self.location.x, start_x, end_x)
        max_x = max(self.location.x, start_x, end_x)
        min_y = min(self.location.y, start_y, end_y)
        max_y = max(self.location.y, start_y, end_y)
        
        self.location.x = min_x
        self.location.y = min_y

        self.corner = self.location.copy()
        self.corner.x = max_x
        self.corner.y = max_y

        # print( )
        # print( self.rawdata )
        # print( )
        
        # print("SchArc - BoundingBox")
        # print(f"Start: {self.location}")
        # print(f"Radius: {self.radius}")
        # print(f"Angle: {self.angle_start} - {self.angle_end}")
        
        # print(f"Bounding: {min_x};{min_y} - {max_x};{max_y}")
            
        return [self.location, self.corner]

    
    def draw(self, graphic, offset, zoom):
        """
        Draw Element using ImageDraw Module of Pillow with support for zoom and offsetting.
        """

        loc_x = (self.location.x * zoom) + offset.x
        loc_y = (self.location.y * zoom) + offset.y
        corner_x = (self.corner.x * zoom) + offset.x
        corner_y = (self.corner.y * zoom) + offset.y
            
        top_left_x = min(float(loc_x), float(corner_x))
        top_left_y = min(float(loc_y), float(corner_y))
        bottom_right_x = max(float(loc_x), float(corner_x))
        bottom_right_y = max(float(loc_y), float(corner_y))
    
        graphic.arc(
            [top_left_x, top_left_y, bottom_right_x, bottom_right_y],
            start = self.angle_start + 180.0,
            end = self.angle_end  + 180.0,
            fill=self.color.to_hex(),
            width= int(self.linewidth),
        )


        
    



