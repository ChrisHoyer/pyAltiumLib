from pyaltiumlib.schlib.records.base import GenericSchRecord
from typing import Optional

# Set up logging
import logging
logger = logging.getLogger(__name__)

class SchParameter(GenericSchRecord):
    """
    Implementation of a schematic record
    See also :ref:`SchPrimitive41` details on this schematic records.
    
    :param Dict data: Dictionary containing raw record data
    :param class parent: Parent symbol object  
    :raises ValueError: If record id is not valid
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 41:
            logger.warning(f"Error in mapping between record objects and record id! - incorrect id {self.record}")
            
        self.name = self.rawdata.get("name", "")
        self.text = self.rawdata.get("text", "")
        self.font_id = int(self.rawdata.get("fontid", 0))
        self.is_hidden = self.rawdata.get_bool('ishidden')