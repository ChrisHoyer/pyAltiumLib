from pyaltiumlib.schlib.records.base import _GenericSchRecord
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint
from pyaltiumlib.datatypes import SchematicLineWidth
import logging

# Set up logging
logger = logging.getLogger(__name__)

class SchEllipse(_GenericSchRecord):
    """
    A class to represent an ellipse in an Altium Schematic Library.

    Attributes:
        radius_x (Coordinate): The x-radius of the ellipse.
        radius_y (Coordinate): The y-radius of the ellipse.
        linewidth (SchematicLineWidth): The width of the ellipse's border.
        issolid (bool): Whether the ellipse is solid.
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 8:
            raise TypeError("Incorrect assigned schematic record")
            
        self.radius_x = Coordinate.parse_dpx("radius", self.rawdata)
        self.radius_y = Coordinate.parse_dpx("secondaryradius", self.rawdata)                   
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))
        self.issolid = self.rawdata.get_bool('issolid')
        
    def __repr__(self):
        return f"SchEllipse"

    def get_bounding_box(self):
        """
        Return the bounding box for the ellipse.

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
        Draw the ellipse using svgwrite.

        Args:
            dwg: The SVG drawing object.
            offset (CoordinatePoint): The offset for drawing.
            zoom (float): The zoom factor for scaling.
        """
        center = (self.location * zoom) + offset
        radius_x = self.radius_x * zoom
        radius_y = self.radius_y * zoom
        
        dwg.add(dwg.ellipse(center=center.to_int_tuple(),
                            r=(int(radius_x), int(radius_y)),
                            fill=self.areacolor.to_hex() if self.issolid else "none",
                            stroke=self.color.to_hex(),
                            stroke_width=int(self.linewidth) * zoom,
                            stroke_linejoin="round",
                            stroke_linecap="round"))