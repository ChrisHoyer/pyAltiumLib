from pyaltiumlib.schlib.records.base import _GenericSchRecord
from pyaltiumlib.datatypes import SchematicTextOrientation, SchematicTextJustification
from pyaltiumlib.datatypes.coordinate import CoordinatePoint

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class SchLabel(_GenericSchRecord):
    """
    Represents a text label in an Altium schematic library.
    
    Attributes:
        orientation (SchematicTextOrientation): Text orientation
        justification (SchematicTextJustification): Text alignment
        font_id (int): Index of font in parent library
        text (str): Display text content
        is_mirrored (bool): Mirror state
        is_hidden (bool): Visibility state
        alignment (Dict): Text positioning metadata
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 4:
            raise ValueError(f"Invalid record type {self.record} for SchLabel (expected 4)")

        self.orientation = SchematicTextOrientation(self.rawdata.get("orientation", 0))
        self.justification = SchematicTextJustification(self.rawdata.get("justification", 0))
        self.font_id = int(self.rawdata.get("fontid", 0))
        self.text = self.rawdata.get("text", "")
        self.is_mirrored = self.rawdata.get_bool('ismirrored')
        self.is_hidden = self.rawdata.get_bool('ishidden')
        self.alignment: Dict[str, any] = {}
        
        self.is_initialized = True

    def __repr__(self) -> str:
        return f"SchLabel(text='{self.text}')"

    def get_bounding_box(self) -> List[CoordinatePoint]:
        """Calculate bounding box based on text metrics and orientation."""
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
        """Render label text to SVG with proper formatting and alignment."""
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