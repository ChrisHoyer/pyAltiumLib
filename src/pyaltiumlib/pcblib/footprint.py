from pyaltiumlib.libcomponent import LibComponent
from pyaltiumlib.datatypes import ParameterCollection, BinaryReader 
from pyaltiumlib.pcblib.records import *

class PcbLibFootprint(LibComponent):
    
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
                


               

                

                

        
                
        
                   
                
        
            
