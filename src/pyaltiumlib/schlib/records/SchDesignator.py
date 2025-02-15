from pyaltiumlib.schlib.records.base import GenericSchRecord
from pyaltiumlib.datatypes.coordinate import CoordinatePoint

from typing import Tuple

# Set up logging
import logging
logger = logging.getLogger(__name__)

class SchDesignator(GenericSchRecord):
    """
    Implementation of a schematic record
    See also :ref:`SchPrimitive34` details on this schematic records. This record can be drawn if not excluded.
    
    :param Dict data: Dictionary containing raw record data
    :param class parent: Parent symbol object  
    :raises ValueError: If record id is not valid
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 34:
            logger.warning(f"Error in mapping between record objects and record id! - incorrect id {self.record}")

        self.text = self.rawdata.get("text", "")
        self.font_id = int(self.rawdata.get("fontid", 0))
        self.is_hidden = self.rawdata.get_bool('ishidden')
        
        self.is_drawable = True

    def get_bounding_box(self) -> Tuple[CoordinatePoint, CoordinatePoint]:
        """
        Generates and returns a bounding box for this record
        
        :return: List with two coordinate entries 
        :rtype: tuple with :ref:`DataTypeCoordinatePoint`
        """
        if not hasattr(self.Symbol.LibFile, '_Fonts') or self.font_id >= len(self.Symbol.LibFile._Fonts):
            logger.warning(f"Invalid font ID {self.font_id} for label '{self.text}'")
            return [self.location.copy(), self.location.copy()]

        font = self.Symbol.LibFile._Fonts[self.font_id]

        start = self.location.copy()
        end = self.location.copy()
        end.x += len(self.text) * font.size * 0.6
        end.y -= font.size

        return [start, end]
    
    def draw_svg(self, dwg, offset, zoom) -> None:
        """
        Draw schematic record using svgwrite.
        
        :param graphic dwg: svg drawing object
        :param CoordinatePoint offset: Move drawing by the given offset as :ref:`DataTypeCoordinatePoint`
        :param float zoom: Scaling Factor for all elements  
        """
        if self.is_hidden:
            return

        try:
            font = self.Symbol.LibFile._Fonts[self.font_id]
        except IndexError:
            logger.error(f"Missing font ID {self.font_id} for label '{self.text}'")
            return

        insert = (self.location * zoom) + offset

        dwg.add(dwg.text(
            self.text,
            insert=insert.to_int_tuple(),
            font_size=font.size * zoom,
            fill=self.color.to_hex(),
            dominant_baseline="text-after-edge",
            text_anchor="start",
        ))