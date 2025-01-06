from pyaltiumlib.schlib.records.base import _SchCommonParam
from pyaltiumlib.datatypes import ( SchCoord, SchCoordPoint, 
                                   SchematicLineWidth, SchematicLineStyle )

class SchLine(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 13 ):
            raise TypeError("Incorrect assigned schematic record")
            
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))             
        self.linestyle = SchematicLineStyle(self.rawdata.get('linestyle', 0)) 
        
        self.corner = SchCoordPoint(SchCoord.parse_dpx("corner.x", self.rawdata),
                                     SchCoord.parse_dpx("corner.y", self.rawdata, scale=-1.0))           
        
    def __repr__(self):
        return f"SchLine "        
        

# =============================================================================
#     Drawing related
# =============================================================================   
         
    def get_bounding_box(self):
        """
        Return bounding box for the object, including all coordinates from
        self.location and self.vertices.
        """    
        min_x = min(float(self.corner.x), float(self.location.x))
        min_y = min(float(self.corner.y), float(self.location.y))
        max_x = max(float(self.corner.x), float(self.location.x))
        max_y = max(float(self.corner.y), float(self.location.y))
        
        # print( )
        # print( self.rawdata )
        # print( )
        
        # print("SchPolyline - BoundingBox")
        # print(f"Start: {self.location}")
        
        # print(f"Bounding: {min_x};{min_y} - {max_x};{max_y}")

        return [SchCoordPoint(SchCoord(min_x), SchCoord(min_y)),
                SchCoordPoint(SchCoord(max_x), SchCoord(max_y))]


    
    def draw(self, graphic, offset, zoom):
        """
        Draw Element using ImageDraw Module of Pillow with support for zoom and offsetting.
        """

        loc_x = float( (self.location.x * zoom) + offset.x )
        loc_y = float( (self.location.y * zoom) + offset.y )
        corner_x = float( (self.corner.x * zoom) + offset.x )
        corner_y = float( (self.corner.y * zoom) + offset.y )

        graphic.line(
            [loc_x, loc_y, corner_x, corner_y],
            fill=self.color.to_hex(),
            width=int(self.linewidth),
        )
            
