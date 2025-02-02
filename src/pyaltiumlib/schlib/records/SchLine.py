from pyaltiumlib.schlib.records.base import _GenericSchRecord
from pyaltiumlib.datatypes import SchematicLineWidth, SchematicLineStyle
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint

import logging
from typing import List

logger = logging.getLogger(__name__)

class SchLine(_GenericSchRecord):
    """
    Represents a straight line in an Altium schematic library.
    
    Attributes:
        linewidth (SchematicLineWidth): Stroke width
        linestyle (SchematicLineStyle): Stroke pattern
        corner (CoordinatePoint): End point coordinates
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 13:
            raise ValueError(f"Invalid record type {self.record} for SchLine (expected 13)")

        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))
        self.linestyle = SchematicLineStyle(self.rawdata.get('linestyle', 0))
        self.linestyle_ext = SchematicLineStyle(self.rawdata.get('linestyleext', 0))
        
        self.corner = CoordinatePoint(
            Coordinate.parse_dpx("corner.x", self.rawdata),
            Coordinate.parse_dpx("corner.y", self.rawdata, scale=-1.0)
        )
        
        self.is_initialized = True

    def __repr__(self) -> str:
        return f"SchLine({self.location} to {self.corner})"

    def get_bounding_box(self) -> List[CoordinatePoint]:
        """Calculate bounding box including line width buffer."""
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
        """Render line to SVG with proper styling."""
        start = (self.location * zoom) + offset
        end = (self.corner * zoom) + offset
        
        dwg.add(dwg.line(
            start=start.to_int_tuple(),
            end=end.to_int_tuple(),
            stroke=self.color.to_hex(),
            stroke_width=int(self.linewidth) * zoom,
            stroke_dasharray=self.draw_linestyle(),
            stroke_linecap="round",
            stroke_linejoin="round"
        ))