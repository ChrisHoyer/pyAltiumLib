from pyaltiumlib.schlib.records.base import _GenericSchRecord
import logging

# Set up logging
logger = logging.getLogger(__name__)

class SchDesignator(_GenericSchRecord):
    """
    A class to represent a designator in an Altium Schematic Library.

    Attributes:
        None: This class currently does not have additional attributes.
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 34:
            raise TypeError("Incorrect assigned schematic record")
            
    def __repr__(self):
        return f"SchDesignator"

    def get_bounding_box(self):
        """
        Return the bounding box for the designator.

        Returns:
            None: Designators do not have a bounding box.
        """
        return None

    def draw_svg(self, dwg, offset, zoom):
        """
        Draw the designator using svgwrite.

        Args:
            dwg: The SVG drawing object.
            offset (CoordinatePoint): The offset for drawing.
            zoom (float): The zoom factor for scaling.
        """
        return None