from pyaltiumlib.libcomponent import LibComponent
from pyaltiumlib.datatypes import ParameterCollection, BinaryReader 
from pyaltiumlib.pcblib.records import *

# Set up logging
import logging
logger = logging.getLogger(__name__)

class PcbLibFootprint(LibComponent):
    """
    Footprint class represent a PCb footprint in an Altium Schematic Library.
    This class is derived from :class:`pyaltiumlib.libcomponent.LibComponent`. 
    
    During initialization the library file will be read.
    
    :param class parent: reference to library file :class:`pyaltiumlib.schlib.lib.PCBLib`
    :param string name: name of the component
    :param string description: description of the component

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

        self.RecordCount = int.from_bytes(self.LibFile._OpenStream(self.Name,  "Header").read(),
                                          "little")

        olestream = self.LibFile._OpenStream(self.Name,  "Data")
        
        name = BinaryReader.from_stream( olestream ).read_string_block()

        StreamOnGoing = True
        while StreamOnGoing: 
            
            RecordID = int.from_bytes( olestream.read(1), "little" )

            if RecordID == 0:
                StreamOnGoing = False
                break
                
            elif RecordID == 2:
                self.Records.append( PcbPad(self, olestream) )
                
            elif RecordID == 4:
                self.Records.append( PcbTrack(self, olestream) )
                
            elif RecordID == 5:
                self.Records.append( PcbString(self, olestream) )
                
            elif RecordID == 12:
                self.Records.append( PcbComponentBody(self, olestream) )

            else:
                print(f"RecordID: {RecordID}")
                


               

                

                

        
                
        
                   
                
        
            
