from pyaltiumlib.schlib.records.base import GenericSchRecord

# Set up logging
import logging
logger = logging.getLogger(__name__)

class SchImplementationList(GenericSchRecord):
    """
    A class to represent an implementation list in an Altium Schematic Library.

    Attributes:
        None: This class currently does not have additional attributes.
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 44:
            raise TypeError("Incorrect assigned schematic record")
            