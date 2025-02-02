"""
Base class for schematic records in Altium libraries.
Provides common functionality for all schematic record types.
"""

from pyaltiumlib.datatypes import ParameterColor
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint
import logging
from typing import Dict, Any, Optional, Tuple

# Configure logging
logger = logging.getLogger(__name__)

class _GenericSchRecord:
    """
    Base class for all schematic records in Altium libraries.
    
    Attributes:
        Symbol: Parent symbol object.
        rawdata: Raw data dictionary for the record.
        record: Record type identifier.
        is_not_accessible: Whether the record is inaccessible.
        graphically_locked: Whether the record is graphically locked.
        owner_index: Index of the owner component.
        owner_part_id: ID of the owner part.
        owner_part_display_mode: Display mode of the owner part.
        unique_id: Unique identifier for the record.
        location: Position of the record in schematic coordinates.
        color: Stroke color of the record.
        areacolor: Fill color of the record.
        spacing_label_name: Spacing for name labels.
        spacing_label_designator: Spacing for designator labels.
    """

    def __init__(self, data: Dict[str, Any], parent: Optional[Any] = None):
        """
        Initialize a schematic record with raw data and parent reference.
        
        Args:
            data: Dictionary containing raw record data.
            parent: Parent symbol object (optional).
        """
        self.Symbol = parent
        self.rawdata = data
        self.is_initialized = False

        # Parse record metadata
        self.record = int(self.rawdata.get('record', 0))
        self.is_not_accessible = self.rawdata.get_bool('isnotaccessible', False)
        self.graphically_locked = self.rawdata.get_bool('graphicallylocked', False)
        
        # Parse ownership information
        self.owner_index = int(self.rawdata.get('ownerindex', 0))
        self.owner_part_id = self.rawdata.get('ownerpartid', '0') == '1'
        self.owner_part_display_mode = int(self.rawdata.get('ownerpartdisplaymode', 0))
        self.unique_id = self.rawdata.get('uniqueid', '')

        # Parse location and colors
        self.location = CoordinatePoint(
            Coordinate.parse_dpx("location.x", self.rawdata),
            Coordinate.parse_dpx("location.y", self.rawdata, scale=-1.0)
        )
        self.color = ParameterColor(self.rawdata.get('color', 0))
        self.areacolor = ParameterColor(self.rawdata.get('areacolor', 0))

        # Default spacing values
        self.spacing_label_name = 4.0
        self.spacing_label_designator = 1.0


    def draw_linestyle(self) -> str:
        """
        Generate SVG stroke dasharray for the record's line style.
        
        Returns:
            str: SVG-compatible dasharray string.
        
        Raises:
            AttributeError: If neither 'linestyle' nor 'linestyle_ext' is defined.
        """
        if not hasattr(self, 'linestyle') and not hasattr(self, 'linestyle_ext'):
            logger.error("Object must have either 'linestyle' or 'linestyle_ext' attribute")
            raise

        # Determine line style
        style_value = getattr(self, 'linestyle', getattr(self, 'linestyle_ext')).to_int()
        
        if style_value == 1:  # Dotted
            return "4,10"
        elif style_value == 2:  # Dashed
            return "1,10"
        elif style_value == 3:  # Dash-dotted
            return "1,10,4,10"
        else:  # Solid
            return "none"

    def draw_bounding_box(self, graphic, offset: CoordinatePoint, zoom: float) -> None:
        """
        Draw a bounding box around the record using SVG.
        
        Args:
            graphic: SVG drawing object.
            offset: Offset for drawing.
            zoom: Zoom factor for scaling.
        
        Raises:
            ValueError: If bounding box dimensions are invalid.
        """
        try:
            bbox = self.get_bounding_box()
            if bbox is None:
                logger.warning("No bounding box available for record")
                return

            start = (bbox[0] * zoom) + offset
            end = (bbox[1] * zoom) + offset
            size = start - end
            start.y -= size.y

            # Validate dimensions
            if size.y == 0 or size.x == 0:
                logger.error(f"Invalid bounding box dimensions: {size}")
                raise

            # Add rectangle to SVG
            graphic.add(
                graphic.rect(
                    insert=start.get_int(),
                    size=[abs(x) for x in size.get_int()],
                    fill="none",
                    stroke="black",
                    stroke_width=1
                )
            )
        except Exception as e:
            logger.error(f"Failed to draw bounding box: {str(e)}")
            raise