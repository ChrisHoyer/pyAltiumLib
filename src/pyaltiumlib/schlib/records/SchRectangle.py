from pyaltiumlib.datatypes import SchematicLineWidth, SchematicLineStyle
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint
from pyaltiumlib.schlib.records.base import _GenericSchRecord

class SchRectangle(_GenericSchRecord):
    
    def __init__(self, data, parent):
       
        super().__init__(data, parent)
        
        if not( self.record == 14 ):
            raise TypeError("Incorrect assigned schematic record")
            
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))             
        self.transparent = self.rawdata.get_bool("transparent") 
        self.issolid = self.rawdata.get_bool("issolid")
        self.linestyle = SchematicLineStyle(self.rawdata.get('linestyle', 0))
        self.linestyle_ext = SchematicLineStyle(self.rawdata.get('linestyleext', 0))
        
        self.corner =  CoordinatePoint(Coordinate.parse_dpx("corner.x", self.rawdata),
                                       Coordinate.parse_dpx("corner.y", self.rawdata, scale=-1.0))               
                    
    def __repr__(self):
        return f"SchRectangle "        

# =============================================================================
#     Drawing related
# =============================================================================   
         
    def get_bounding_box(self):
        """
        Return bounding box for the object
        """
         
        return [self.location, self.corner]

    
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
        
        start = (self.location * zoom) + offset
        end = (self.corner * zoom) + offset
        
        # start is lower left corner -> needs to be upper right
        size = start - end
        start.y = start.y - size.y

        dwg.add(dwg.rect(insert = start.get_int(),
                         size = [ abs(x) for x in size.get_int() ],
                         fill = self.areacolor.to_hex() if self.issolid else "none",
                         stroke = self.color.to_hex(),
                         stroke_dasharray = self.draw_linestyle(),
                         stroke_width = int(self.linewidth) * zoom,
                         stroke_linejoin="round",
                         stroke_linecap="round"
                         ))





