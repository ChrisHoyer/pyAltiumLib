from pyaltiumlib.schlib.records.base import _SchCommonParam
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint
from pyaltiumlib.datatypes import SchematicLineWidth

class SchEllipse(_SchCommonParam):
    
    def __init__(self, data, parent):
       
        super().__init__(data, parent)
        
        if not( self.record == 8 ):
            raise TypeError("Incorrect assigned schematic record")
            
        self.radius_x = Coordinate.parse_dpx("radius", self.rawdata)
        self.radius_y = Coordinate.parse_dpx("secondaryradius", self.rawdata)                   
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))
        self.issolid = self.rawdata.get_bool('issolid')
        
    def __repr__(self):
        return f"SchEllipse "        
        
# =============================================================================
#     Drawing related
# ============================================================================= 
    def get_bounding_box(self):
        """
        Return bounding box for the object
        """

        start_x = self.location.x - self.radius_x
        start_y = self.location.y - self.radius_y        
        end_x = self.location.x + self.radius_x
        end_y = self.location.y + self.radius_y

        min_x = min(self.location.x, start_x, end_x)
        max_x = max(self.location.x, start_x, end_x)
        min_y = min(self.location.y, start_y, end_y)
        max_y = max(self.location.y, start_y, end_y)
        
        return [CoordinatePoint(min_x, min_y), CoordinatePoint(max_x, max_y)]

    
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

        center = (self.location * zoom) + offset
        radius_x = self.radius_x * zoom
        radius_y = self.radius_y * zoom
        
        dwg.add(dwg.ellipse(center = center.get_int(),
                            r = (int(radius_x), int(radius_y)),
                            fill = self.areacolor.to_hex() if self.issolid else "none",
                            stroke = self.color.to_hex(),
                            stroke_width = int(self.linewidth) * zoom,
                            stroke_linejoin="round",
                            stroke_linecap="round"
                            ))


        
    



