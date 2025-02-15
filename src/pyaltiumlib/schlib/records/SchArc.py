from pyaltiumlib.schlib.records.base import GenericSchRecord
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint
from pyaltiumlib.datatypes import SchematicLineWidth

from typing import Tuple

# Set up logging
import logging
logger = logging.getLogger(__name__)

class SchArc(GenericSchRecord):
    """
    Implementation of a schematic record
    See also :ref:`SchPrimitive12` details on this schematic records. This record can be drawn.
    
    :param Dict data: Dictionary containing raw record data
    :param class parent: Parent symbol object  
    :raises ValueError: If record id is not valid
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 12:
            logger.warning(f"Error in mapping between record objects and record id! - incorrect id {self.record}")
            
        self.radius = Coordinate.parse_dpx("radius", self.rawdata)
        self.angle_start = float(self.rawdata.get('startangle', 0))
        self.angle_end = float(self.rawdata.get('endangle', 0))
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))
        
        self.is_drawable = True

    def get_bounding_box(self) -> Tuple[CoordinatePoint, CoordinatePoint]:
        """
        Generates and returns a bounding box for this record
        
        :return: List with two coordinate entries 
        :rtype: tuple with :ref:`DataTypeCoordinatePoint`
        """
        start_x = self.location.x - self.radius
        start_y = self.location.y - self.radius
        end_x = self.location.x + self.radius
        end_y = self.location.y + self.radius

        min_x = min(self.location.x, start_x, end_x)
        max_x = max(self.location.x, start_x, end_x)
        min_y = min(self.location.y, start_y, end_y)
        max_y = max(self.location.y, start_y, end_y)
        
        return [CoordinatePoint(min_x, min_y), CoordinatePoint(max_x, max_y)]

    def draw_svg(self, dwg, offset, zoom) -> None:
        """
        Draw schematic record using svgwrite.
        
        :param graphic dwg: svg drawing object
        :param CoordinatePoint offset: Move drawing by the given offset as :ref:`DataTypeCoordinatePoint`
        :param float zoom: Scaling Factor for all elements  
        """
        center = (self.location * zoom) + offset
        radius = self.radius * zoom
        
        arc_path = self.get_svg_arc_path(center.to_int_tuple(),
                                         int(radius), int(radius),
                                         self.angle_start, self.angle_end)

        dwg.add(dwg.path(d=arc_path,
                         fill="none",
                         stroke=self.color.to_hex(),
                         stroke_width=int(self.linewidth) * zoom,
                         stroke_linejoin="round",
                         stroke_linecap="round"))

