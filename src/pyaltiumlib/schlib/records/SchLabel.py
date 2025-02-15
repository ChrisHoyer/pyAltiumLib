from pyaltiumlib.schlib.records.base import GenericSchRecord
from pyaltiumlib.datatypes import SchematicTextOrientation, SchematicTextJustification
from pyaltiumlib.datatypes.coordinate import CoordinatePoint

from typing import Dict, Tuple

# Set up logging
import logging
logger = logging.getLogger(__name__)

class SchLabel(GenericSchRecord):
    """
    Implementation of a schematic record
    See also :ref:`SchPrimitive04` details on this schematic records. This record can be drawn.
    
    :param Dict data: Dictionary containing raw record data
    :param class parent: Parent symbol object   
    :raises ValueError: If record id is not valid
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 4:
            logger.warning(f"Error in mapping between record objects and record id! - incorrect id {self.record}")

        self.orientation = SchematicTextOrientation(self.rawdata.get("orientation", 0))
        self.justification = SchematicTextJustification(self.rawdata.get("justification", 0))
        self.font_id = int(self.rawdata.get("fontid", 0))
        self.text = self.rawdata.get("text", "")
        self.is_mirrored = self.rawdata.get_bool('ismirrored')
        self.is_hidden = self.rawdata.get_bool('ishidden')
        self.alignment: Dict[str, any] = {}
        
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
        self.alignment = {
            "vertical": self.justification.get_vertical(),
            "horizontal": self.justification.get_horizontal(),
            "rotation": self.orientation.to_int() * -90,
            "position": self.location.copy()
        }

        # Calculate text dimensions
        char_width = font.size * 0.6
        width = len(self.text) * char_width
        height = font.size

        # Calculate bounding box based on orientation
        orientation = self.orientation.to_int()
        start = self.location.copy()
        end = self.location.copy()

        if orientation == 0:  # 0 degrees
            end.x += width
            end.y -= height
        elif orientation == 1:  # 90 degrees
            start.x -= height
            end.y -= width
        elif orientation == 2:  # 180 degrees
            start.x -= width
            start.y += height
        elif orientation == 3:  # 270 degrees
            end.x -= height
            start.y += width

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
        transform=f"rotate({self.alignment['rotation']} {int(insert.x)} {int(insert.y)})"

        dwg.add(dwg.text(
            self.text,
            insert=insert.to_int_tuple(),
            font_size=font.size * zoom,
            font_family=font.font,
            font_weight=font.bold,
            font_style=font.style,
            text_decoration=font.text_decoration,
            fill=self.color.to_hex(),
            dominant_baseline=self.alignment["vertical"],
            text_anchor=self.alignment["horizontal"],
            transform=transform
        ))