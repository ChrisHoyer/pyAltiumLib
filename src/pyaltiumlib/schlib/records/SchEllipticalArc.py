from pyaltiumlib.schlib.records.base import _GenericSchRecord
from pyaltiumlib.datatypes import SchematicLineWidth
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint
import math


class SchEllipticalArc(_GenericSchRecord):
    
    def __init__(self, data, parent):
       
        super().__init__(data, parent)
        
        if not( self.record == 11 ):
            raise TypeError("Incorrect assigned schematic record")
            
        self.radius_x = Coordinate.parse_dpx("radius", self.rawdata)
        self.radius_y = Coordinate.parse_dpx("secondaryradius", self.rawdata)        
        self.angle_start = float( self.rawdata.get('startangle', 0) )            
        self.angle_end = float( self.rawdata.get('endangle', 0) )            
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0)) 
        
    def __repr__(self):
        return f"SchEllipticalArc "        
        
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
        
        arc_path = self.get_arc_path(center.get_int(), int(radius_x), int(radius_y))

        dwg.add(dwg.path(d = arc_path,
                         fill = "none",
                         stroke = self.color.to_hex(),
                         stroke_width = int(self.linewidth) * zoom
                         ))


    def get_arc_path(self, center, radius_x, radius_y):
 
        def degrees_to_radians(degrees):
            radians = degrees * math.pi / 180
            return radians % (2*math.pi)       
         
        angle_start = degrees_to_radians(self.angle_start)
        angle_stop = degrees_to_radians(self.angle_end)
        
        if angle_start == angle_stop:
                angle_stop -= 0.001
            
        start_x = center[0] + radius_x * math.cos(-angle_start)
        start_y = center[1] + radius_y * math.sin(-angle_start)
        end_x = center[0] + radius_x * math.cos(-angle_stop)
        end_y = center[1] + radius_y * math.sin(-angle_stop)
        
        # Set large_arc_flag based on the angle difference
        large_arc_flag = 1 if (angle_stop - angle_start) % (2 * math.pi) > math.pi else 0
        
        # Set sweep_flag to 0 for counterclockwise
        sweep_flag = 0
        
        path_data = (
            f"M {start_x},{start_y} "
            f"A {radius_x},{radius_y} 0 {large_arc_flag},{sweep_flag} {end_x},{end_y}"
            )
        return path_data          
    



