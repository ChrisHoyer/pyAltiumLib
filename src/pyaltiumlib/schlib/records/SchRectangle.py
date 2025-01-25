from pyaltiumlib.schlib.records.base import _GenericSchRecord
from pyaltiumlib.datatypes import SchematicLineWidth, SchematicLineStyle
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint

import logging

# Set up logging
logger = logging.getLogger(__name__)

class SchRectangle(_GenericSchRecord):
    """
    A class to represent a rectangle in an Altium Schematic Library.

    Attributes:
        linewidth (SchematicLineWidth): The width of the rectangle's border.
        transparent (bool): Whether the rectangle is transparent.
        issolid (bool): Whether the rectangle is solid.
        linestyle (SchematicLineStyle): The line style of the rectangle.
        linestyle_ext (SchematicLineStyle): The extended line style of the rectangle.
        corner (CoordinatePoint): The opposite corner of the rectangle.
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 14:
            raise TypeError("Incorrect assigned schematic record")
            
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))             
        self.transparent = self.rawdata.get_bool("transparent") 
        self.issolid = self.rawdata.get_bool("issolid")
        self.linestyle = SchematicLineStyle(self.rawdata.get('linestyle', 0))
        self.linestyle_ext = SchematicLineStyle(self.rawdata.get('linestyleext', 0))
        
        self.corner = CoordinatePoint(Coordinate.parse_dpx("corner.x", self.rawdata),
                                       Coordinate.parse_dpx("corner.y", self.rawdata, scale=-1.0))               
                    
    def __repr__(self):
        return f"SchRectangle"

    def get_bounding_box(self):
        """
        Return the bounding box for the rectangle.

        Returns:
            List[CoordinatePoint]: The bounding box as a list of two CoordinatePoints.
        """
        return [self.location, self.corner]

    def draw_svg(self, dwg, offset, zoom):
        """
        Draw the rectangle using svgwrite.

        Args:
            dwg: The SVG drawing object.
            offset (CoordinatePoint): The offset for drawing.
            zoom (float): The zoom factor for scaling.
        """
        start = (self.location * zoom) + offset
        end = (self.corner * zoom) + offset
        
        # start is lower left corner -> needs to be upper right
        size = start - end
        start.y = start.y - size.y

        dwg.add(dwg.rect(insert=start.to_int_tuple(),
                         size=[abs(x) for x in size.to_int_tuple()],
                         fill=self.areacolor.to_hex() if self.issolid else "none",
                         stroke=self.color.to_hex(),
                         stroke_dasharray=self.draw_linestyle(),
                         stroke_width=int(self.linewidth) * zoom,
                         stroke_linejoin="round",
                         stroke_linecap="round"))