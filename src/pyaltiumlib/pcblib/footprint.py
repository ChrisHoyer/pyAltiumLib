from pyaltiumlib.libcomponent import LibComponent
from pyaltiumlib.datatypes import ParameterCollection, BinaryReader 
from pyaltiumlib.pcblib.records import *

# Set up logging
import logging
logger = logging.getLogger(__name__)

class PcbLibFootprint(LibComponent):
    """
    Footprint class represent a PCB footprint in an Altium Schematic Library.
    During initialization the library file will be read.
    
    :param class parent: reference to library file :class:`pyaltiumlib.schlib.lib.PCBLib`
    :param string name: name of the component
    :param string optional description: description of the component

    :raises ValueError: If record id is not valid
    :raises ValueError: If component data can not be read
    """   
    def __init__(self, parent, name, description=""):

        super().__init__(parent, name, description)
                
        self._ReadFootprintParameters()  
        self._ReadFootprintData()
        
# =============================================================================
#     Internal content reading related functions
# =============================================================================   
 
    def _ReadFootprintParameters(self):
        
        self._Parameters = ParameterCollection.from_block( 
            self.LibFile._OpenStream(self.Name,  "Parameters")  )
        
        self.Description = self._Parameters.get("description")


    def _ReadFootprintData(self):

        self._RecordCount = int.from_bytes(self.LibFile._OpenStream(self.Name,  "Header").read(),
                                          "little")

        try:
            olestream = self.LibFile._OpenStream(self.Name,  "Data")
            
            name = BinaryReader.from_stream( olestream ).read_string_block()
    
            StreamOnGoing = True
            while StreamOnGoing: 
                
                RecordID = int.from_bytes( olestream.read(1), "little" )
                
                if RecordID == 0:
                    StreamOnGoing = False
                    break
    
                elif RecordID == 1:
                    self.Records.append( PcbArc(self, olestream) )
                    
                elif RecordID == 2:
                    self.Records.append( PcbPad(self, olestream) )

                elif RecordID == 3:
                    self.Records.append( PcbVia(self, olestream) )
                    
                elif RecordID == 4:
                    self.Records.append( PcbTrack(self, olestream) )
                    
                elif RecordID == 5:
                    self.Records.append( PcbString(self, olestream) )

                elif RecordID == 6:
                    self.Records.append( PcbFill(self, olestream) )   

                elif RecordID == 11:
                    self.Records.append( PcbRegion(self, olestream) )   

                elif RecordID == 12:
                    self.Records.append( PcbComponentBody(self, olestream) ) 
                     
                else:
                    logger.warning(f"Found unsupported RecordID={RecordID} in '{self.Name}'.")

        except Exception as e:
            logger.error(f"Failed to read data of '{self.Name}'. Exception: {e}")
            raise                


               

                

                

        
                
        
                   
                
        
            
