from pyaltiumlib.schlib.records.base import _GenericSchRecord
from pyaltiumlib.datatypes import SchematicLineWidth, SchematicLineStyle
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint

class SchLine(_GenericSchRecord):
    
    def __init__(self, data, parent):
       
        super().__init__(data, parent)
        
        if not( self.record == 13 ):
            raise TypeError("Incorrect assigned schematic record")
            
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))             
        self.linestyle = SchematicLineStyle(self.rawdata.get('linestyle', 0))
        self.linestyle_ext = SchematicLineStyle(self.rawdata.get('linestyleext', 0))
         
        self.corner = CoordinatePoint(Coordinate.parse_dpx("corner.x", self.rawdata),
                                      Coordinate.parse_dpx("corner.y", self.rawdata, scale=-1.0))           
        
    def __repr__(self):
        return f"SchLine "        
        

# =============================================================================
#     Drawing related
# =============================================================================   
         
    def get_bounding_box(self):
        """
        Return bounding box for the object
        """
        
        half_width = int(self.linewidth) / 2
        
        min_x = min(float(self.location.x), float(self.corner.x)) - half_width
        min_y = min(float(self.location.y), float(self.corner.y)) - half_width
        max_x = max(float(self.location.x), float(self.corner.x)) + half_width
        max_y = max(float(self.location.y), float(self.corner.y)) + half_width
        
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

        start = (self.location * zoom) + offset
        end = (self.corner * zoom) + offset
            
        dwg.add(dwg.line(start = start.to_int_tuple(),
                         end = end.to_int_tuple(),
                         stroke_dasharray = self.draw_linestyle(),
                         stroke = self.color.to_hex(),
                         stroke_width = int(self.linewidth) * zoom,
                         stroke_linejoin="round",
                         stroke_linecap="round"
                         ))
            
