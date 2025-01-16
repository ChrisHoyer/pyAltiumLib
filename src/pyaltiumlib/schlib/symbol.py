

from pyaltiumlib.libcomponent import LibComponent
from pyaltiumlib.datatypes import ParameterCollection, SchematicPin
from pyaltiumlib.schlib.records import *


class SchLibSymbol(LibComponent):
    
    def __init__(self, parent, name, description="", partcount = 0):

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
 
        
    def _CreateRecord(self, record):
        
        RecordId = record.get_record()
        if RecordId is None:
            raise ValueError("No 'recordid' found.")
                
        if int(RecordId) == 1:
            self.Records.append( SchComponent(record, self) )
            
        elif int(RecordId) == 2:
            self.Records.append( SchPin(record, self) )

        elif int(RecordId) == 4:
            self.Records.append( SchLabel(record, self) )  

        elif int(RecordId) == 5:
            self.Records.append( SchBezier(record, self) )  
            
        elif int(RecordId) == 6:
            self.Records.append( SchPolyline(record, self) )    

        elif int(RecordId) == 7:
            self.Records.append( SchPolygon(record, self) )   

        elif int(RecordId) == 8:
            self.Records.append( SchEllipse(record, self) ) 

        elif int(RecordId) == 10:
            self.Records.append( SchRoundRectangle(record, self) )
            
        elif int(RecordId) == 11:
            self.Records.append( SchEllipticalArc(record, self) )   
            
        elif int(RecordId) == 12:
            self.Records.append( SchArc(record, self) )            

        elif int(RecordId) == 13:
            self.Records.append( SchLine(record, self) ) 
            
        elif int(RecordId) == 14:
            self.Records.append( SchRectangle(record, self) )

        elif int(RecordId) == 34:
            self.Records.append( SchDesignator(record, self) )
            
        elif int(RecordId) == 41:
            self.Records.append( SchParameter(record, self) )

        elif int(RecordId) == 44:
            self.Records.append( SchImplementationList(record, self) )
            
        else:
             print(f"Unsupported record id value: {RecordId}")
        

    def _ReadSymbolData(self):
        
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
                

                

                

        
                
        
                   
                
        
            
