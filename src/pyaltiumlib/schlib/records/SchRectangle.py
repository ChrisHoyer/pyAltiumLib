from pyaltiumlib.datatypes import SchCoord, SchCoordPoint, SchematicLineWidth
from pyaltiumlib.schlib.records.base import _SchCommonParam

class SchRectangle(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 14 ):
            raise TypeError("Incorrect assigned schematic record")
            
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))             
        self.transparent = bool( self.rawdata.get("transparent", "F").upper() == "T" )
        self.issolid = bool( self.rawdata.get("issolid", "F").upper() == "T" )
        
        self.corner =  SchCoordPoint(SchCoord.parse_dpx("corner.x", self.rawdata),
                                     SchCoord.parse_dpx("corner.y", self.rawdata, scale=-1.0))               
                    
    def __repr__(self):
        return f"SchRectangle "        

# =============================================================================
#     Drawing related
# =============================================================================   
         
    def get_bounding_box(self, InvertY=False):
        """
        Return bounding box
        """            
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
    
        graphic.rectangle(
            [top_left_x, top_left_y, bottom_right_x, bottom_right_y],
            outline=self.color.to_hex(),
            width= int(self.linewidth),
            fill=self.areacolor.to_hex(),
        )






