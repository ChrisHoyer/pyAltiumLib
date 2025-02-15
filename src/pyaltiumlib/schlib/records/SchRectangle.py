from pyaltiumlib.schlib.records.base import GenericSchRecord
from pyaltiumlib.datatypes import SchematicLineWidth, SchematicLineStyle
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint

from typing import Tuple

# Set up logging
import logging
logger = logging.getLogger(__name__)

class SchRectangle(GenericSchRecord):
    """
    Implementation of a schematic record
    See also :ref:`SchPrimitive14` details on this schematic records. This record can be drawn.
    
    :param Dict data: Dictionary containing raw record data
    :param class parent: Parent symbol object  
    :raises ValueError: If record id is not valid
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 14:
            logger.warning(f"Error in mapping between record objects and record id! - incorrect id {self.record}")
          
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))             
        self.transparent = self.rawdata.get_bool("transparent") 
        self.issolid = self.rawdata.get_bool("issolid")
        self.linestyle = SchematicLineStyle(self.rawdata.get('linestyle', 0))
        self.linestyle_ext = SchematicLineStyle(self.rawdata.get('linestyleext', 0))
        
        self.corner = CoordinatePoint(Coordinate.parse_dpx("corner.x", self.rawdata),
                                       Coordinate.parse_dpx("corner.y", self.rawdata, scale=-1.0))  

        self.is_drawable = True             

    def get_bounding_box(self) -> Tuple[CoordinatePoint, CoordinatePoint]:
        """
        Generates and returns a bounding box for this record
        
        :return: List with two coordinate entries 
        :rtype: tuple with :ref:`DataTypeCoordinatePoint`
        """
        return [self.location, self.corner]


    def draw_svg(self, dwg, offset, zoom) -> None:
        """
        Draw schematic record using svgwrite.
        
        :param graphic dwg: svg drawing object
        :param CoordinatePoint offset: Move drawing by the given offset as :ref:`DataTypeCoordinatePoint`
        :param float zoom: Scaling Factor for all elements  
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
                         stroke_dasharray=self.get_svg_stroke_dasharray(),
                         stroke_width=int(self.linewidth) * zoom,
                         stroke_linejoin="round",
                         stroke_linecap="round"))