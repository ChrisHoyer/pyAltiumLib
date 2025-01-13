import json

from pyaltiumlib.datatypes import ParameterCollection
from pyaltiumlib.datatypes import BinaryReader
from pyaltiumlib.pcblib.records import *

class PcbLibFootprint:
    
    def __init__(self, parent, name, description=""):

        self.LibFile = parent
        self.Name = str(name)
        self.Description = description
        
        self.Records = [] 
        
        self._ReadFootprintParameters()  
        self._ReadFootprintData()                          
 
        
    def __repr__(self):
        footprint_data = {
           "Name": self.Name,
           "Description": self.Description,
           }
        
        return json.dumps(footprint_data, indent=4)
                  
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
        
        _, name = BinaryReader.from_stream( olestream ).read_string_block()

        StreamOnGoing = True
        while StreamOnGoing: 
            
            RecordID = int.from_bytes( olestream.read(1), "little" )
            
            if RecordID == 0x02:
                self.Records.append( PcbPad(self, olestream) )
                
            
      
        return None
        
 
# =============================================================================
#     Drawing related
# =============================================================================   
 

               

                

                

        
                
        
                   
                
        
            
