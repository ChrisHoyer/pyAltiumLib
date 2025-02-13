from pyaltiumlib.schlib.records.base import GenericSchRecord

# Set up logging
import logging
logger = logging.getLogger(__name__)

class SchDesignator(GenericSchRecord):
    """
    A class to represent a designator in an Altium Schematic Library.

    Attributes:
        None: This class currently does not have additional attributes.
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 34:
            raise TypeError("Incorrect assigned schematic record")