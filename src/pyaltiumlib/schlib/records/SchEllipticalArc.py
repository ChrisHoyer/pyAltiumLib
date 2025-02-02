from pyaltiumlib.schlib.records.base import _GenericSchRecord
from pyaltiumlib.datatypes import SchematicLineWidth
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint
from pyaltiumlib.datatypes.svg_utils import get_arc_path

# Set up logging
import logging
logger = logging.getLogger(__name__)

class SchEllipticalArc(_GenericSchRecord):
    """
    A class to represent an elliptical arc in an Altium Schematic Library.

    Attributes:
        radius_x (Coordinate): The x-radius of the elliptical arc.
        radius_y (Coordinate): The y-radius of the elliptical arc.
        angle_start (float): The starting angle of the arc in degrees.
        angle_end (float): The ending angle of the arc in degrees.
        linewidth (SchematicLineWidth): The width of the arc's border.
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 11:
            raise TypeError("Incorrect assigned schematic record")
            
        self.radius_x = Coordinate.parse_dpx("radius", self.rawdata)
        self.radius_y = Coordinate.parse_dpx("secondaryradius", self.rawdata)        
        self.angle_start = float(self.rawdata.get('startangle', 0))            
        self.angle_end = float(self.rawdata.get('endangle', 0))            
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))
        
        self.is_initialized = True
        
    def __repr__(self):
        return f"SchEllipticalArc"

    def get_bounding_box(self):
        """
        Return the bounding box for the elliptical arc.

        Returns:
            List[CoordinatePoint]: The bounding box as a list of two CoordinatePoints.
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
        Draw the elliptical arc using svgwrite.

        Args:
            dwg: The SVG drawing object.
            offset (CoordinatePoint): The offset for drawing.
            zoom (float): The zoom factor for scaling.
        """
        center = (self.location * zoom) + offset
        radius_x = self.radius_x * zoom
        radius_y = self.radius_y * zoom
        
        arc_path = get_arc_path(center.to_int_tuple(),
                                int(radius_x), int(radius_y),
                                self.angle_start, self.angle_end)

        dwg.add(dwg.path(d=arc_path,
                         fill="none",
                         stroke=self.color.to_hex(),
                         stroke_width=int(self.linewidth) * zoom))
