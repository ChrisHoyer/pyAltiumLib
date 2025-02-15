from pyaltiumlib.schlib.records.base import GenericSchRecord
from pyaltiumlib.datatypes import SchematicLineWidth, SchematicLineStyle
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint

from typing import Tuple

# Set up logging
import logging
logger = logging.getLogger(__name__)

class SchLine(GenericSchRecord):
    """
    Implementation of a schematic record
    See also :ref:`SchPrimitive13` details on this schematic records. This record can be drawn.
    
    :param Dict data: Dictionary containing raw record data
    :param class parent: Parent symbol object  
    :raises ValueError: If record id is not valid
    """
    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 13:
            logger.warning(f"Error in mapping between record objects and record id! - incorrect id {self.record}")

        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))
        self.linestyle = SchematicLineStyle(self.rawdata.get('linestyle', 0))
        self.linestyle_ext = SchematicLineStyle(self.rawdata.get('linestyleext', 0))
        
        self.corner = CoordinatePoint(
            Coordinate.parse_dpx("corner.x", self.rawdata),
            Coordinate.parse_dpx("corner.y", self.rawdata, scale=-1.0)
        )
        
        self.is_drawable = True

    def get_bounding_box(self) -> Tuple[CoordinatePoint, CoordinatePoint]:
        """
        Generates and returns a bounding box for this record
        
        :return: List with two coordinate entries 
        :rtype: tuple with :ref:`DataTypeCoordinatePoint`
        """
        half_width = self.linewidth.value / 2
        return [
            CoordinatePoint(
                min(self.location.x, self.corner.x) - half_width,
                min(self.location.y, self.corner.y) - half_width
            ),
            CoordinatePoint(
                max(self.location.x, self.corner.x) + half_width,
                max(self.location.y, self.corner.y) + half_width
            )
        ]

    def draw_svg(self, dwg, offset, zoom) -> None:
        """
        Draw schematic record using svgwrite.
        
        :param graphic dwg: svg drawing object
        :param CoordinatePoint offset: Move drawing by the given offset as :ref:`DataTypeCoordinatePoint`
        :param float zoom: Scaling Factor for all elements  
        """
        start = (self.location * zoom) + offset
        end = (self.corner * zoom) + offset
        
        dwg.add(dwg.line(
            start=start.to_int_tuple(),
            end=end.to_int_tuple(),
            stroke=self.color.to_hex(),
            stroke_width=int(self.linewidth) * zoom,
            stroke_dasharray=self.get_svg_stroke_dasharray(),
            stroke_linecap="round",
            stroke_linejoin="round"
        ))