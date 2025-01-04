"""



"""

from pyaltiumlib.schlib.records import (
    SchComponent, SchPin, SchLabel, SchBezier, SchPolyline, SchPolygon,
    SchEllipse, SchEllipticalArc, SchArc, SchLine, SchRectangle,
    SchDesignator, SchParameter, SchImplementationList) 

class SchLibSymbol:
    
    def __init__(self, parent, name, description="", partcount=0):

        self.parent = parent
        self.name = name
        self.description = description
        self.partcount = partcount
                    
        self.records = []       
        self._ReadSymbolData()
        
        
    def __repr__(self):
        return f"{self.name}"
 
        
    def _CreateRecord(self, record):
        
        RecordId = next((v for k, v in record.items() if k.lower() == "record"), None)
        if RecordId is None:
            raise ValueError("No 'recordid' found.")
                
        if int(RecordId) == 1:
            self.records.append( SchComponent(record) )
            
        elif int(RecordId) == 2:
            self.records.append( SchPin(record) )

        elif int(RecordId) == 4:
            self.records.append( SchLabel(record) )  

        elif int(RecordId) == 5:
            self.records.append( SchBezier(record) )  
            
        elif int(RecordId) == 6:
            self.records.append( SchPolyline(record) )    

        elif int(RecordId) == 7:
            self.records.append( SchPolygon(record) )   

        elif int(RecordId) == 8:
            self.records.append( SchEllipse(record) ) 
            
        elif int(RecordId) == 11:
            self.records.append( SchEllipticalArc(record) )   
            
        elif int(RecordId) == 12:
            self.records.append( SchArc(record) )            

        elif int(RecordId) == 13:
            self.records.append( SchLine(record) ) 
            
        elif int(RecordId) == 14:
            self.records.append( SchRectangle(record) )

        elif int(RecordId) == 34:
            self.records.append( SchDesignator(record) )
            
        elif int(RecordId) == 41:
            self.records.append( SchParameter(record) )

        elif int(RecordId) == 44:
            self.records.append( SchImplementationList(record) )
            
        else:
             raise ValueError(f"Unsupported value: {RecordId}")
        
# =============================================================================
#     Internal content reading related functions
# =============================================================================   
 

# TODO: Read PinFrac
# TODO: Read PinSymbolLineWidth
# TODO: Read PinWideText
# TODO: Read PinTextData

    def _ReadSymbolData(self):
        
        olestream = self.parent._OpenStream(self.name,  "data")
            
        StreamOnGoing = True
        
        while StreamOnGoing: 
            
            RecordLength = int.from_bytes( olestream.read(2), "little" )
            RecordType = int.from_bytes( olestream.read(2), "big" )

            if RecordLength == 0:
                StreamOnGoing = False
                break
            
            if RecordType == 0:
                Record = self.parent._ParseParameterCollection( olestream.read(RecordLength) )
            
            elif RecordType == 1:
                Record = self.parent._ParseSchematicPin( olestream.read(RecordLength) )

            else:
                raise ValueError(f"Record type: { RecordType } unknown!")                
                
            if Record:
                self._CreateRecord( Record )
                

                

                

        
                
        
            
