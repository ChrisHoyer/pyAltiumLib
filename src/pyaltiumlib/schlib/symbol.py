from pyaltiumlib.libcomponent import LibComponent
from pyaltiumlib.datatypes import ParameterCollection, SchematicPin
from pyaltiumlib.schlib.records import *

from typing import Optional, List, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SchLibSymbol(LibComponent):
    """
    A class to represent a symbol in an Altium Schematic Library.

    Attributes:
        PartCount (int): The number of parts in the symbol.
    """
    
    def __init__(self, parent, name: str, description: str = "", partcount: int = 0):
        """
        Initialize a SchLibSymbol object.

        Args:
            parent: The parent library file.
            name (str): The name of the symbol.
            description (str): The description of the symbol.
            partcount (int): The number of parts in the symbol.
        """
        super().__init__(parent, name, description)
        
        self.PartCount = int(partcount) - 1 if partcount else 0                 
        self._ReadSymbolData()
        
                
# =============================================================================
#     Internal content reading related functions
# =============================================================================   
 
# TODO: Read PinFrac
# TODO: Read PinSymbolLineWidth
# TODO: Read PinWideText
# TODO: Read PinTextData
 
        
    def _CreateRecord(self, record: ParameterCollection) -> None:
        """
        Create a record based on its type.

        Args:
            record (ParameterCollection): The record to process.
        """  
        RecordId = record.get_record()
        if RecordId is None:
            logger.error("No 'recordid' found.")
            raise
                
        record_map = {
            1: SchComponent,
            2: SchPin,
            4: SchLabel,
            5: SchBezier,
            6: SchPolyline,
            7: SchPolygon,
            8: SchEllipse,
            10: SchRoundRectangle,
            11: SchEllipticalArc,
            12: SchArc,
            13: SchLine,
            14: SchRectangle,
            34: SchDesignator,
            41: SchParameter,
            44: SchImplementationList,
        }

        try:
            record_id = int(RecordId)
            if record_id in record_map:
                self.Records.append(record_map[record_id](record, self))
            else:
                logger.warning(f"Unsupported record id value: {RecordId}")
        except ValueError:
            logger.error(f"Invalid RecordId: {RecordId} is not a valid integer")

        
    def _ReadSymbolData(self) -> None:
        """
        Read the symbol data from the library file.
        """
        try:
            olestream = self.LibFile._OpenStream(self.Name,  "data")
                
            StreamOnGoing = True
            while StreamOnGoing: 
                
                RecordLength = int.from_bytes( olestream.read(2), "little" )
                RecordType = int.from_bytes( olestream.read(2), "big" )
    
                if RecordLength == 0:
                    StreamOnGoing = False
                    break
                
                if RecordType == 0:
                    Record = ParameterCollection( olestream.read(RecordLength) )
                
                elif RecordType == 1:
                    Record = SchematicPin( olestream.read(RecordLength) )
    
                else:
                    raise ValueError(f"Record type: { RecordType } unknown!")                
                    
                if Record:
                    self._CreateRecord( Record )
                
        except Exception as e:
            logger.error(f"Failed to read symbol data: {e}")
            raise
                

                

        
                
        
                   
                
        
            
