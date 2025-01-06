"""



"""
import json

from pyaltiumlib.datatypes import (
    ParameterCollection, SchematicPin, SchCoord, SchCoordPoint 
    )
from pyaltiumlib.schlib.records import *


class SchLibSymbol:
    
    def __init__(self, parent, name, description="", partcount = 0):

        self._parent = parent
        self.Name = name
        self.Description = description
        self.PartCount = int(partcount) - 1 if partcount else 0
                    
        self.Records = []       
        self._ReadSymbolData()
        
        
    def __repr__(self):
       symbol_data = {
           "Name": self.Name,
           "Description": self.Description,
           "PartCount": self.PartCount
           }
        
       return json.dumps(symbol_data, indent=4)
   

# =============================================================================
#     Drawing related
# =============================================================================   
 
    
    def draw(self, graphic, size_x, size_y):
        
        #print()
        #print(self.Name)
        
        validObj = []
        for obj in self.Records:
            if hasattr(obj, 'draw') and callable(getattr(obj, 'draw')):
                validObj.append( obj )

        # Get Bounding box
        offset, zoom = self._autoscale( validObj, size_x, size_y)

        for obj in validObj:
            obj.draw( graphic, offset, zoom)
                   

    def _autoscale(self, elements, target_width, target_height, margin=10.0):
        """
        Adjusts the coordinates of elements to fit within the target dimensions using zoom.
        Args:
            elements (list): A list of objects with `get_BoundingBox` method.
            target_width (int): Target image width.
            target_height (int): Target image height.
        Returns:
            tuple: (offset, zoom)
        """

        min_point = SchCoordPoint(SchCoord(float("inf")), SchCoord(float("inf")))
        max_point = SchCoordPoint(SchCoord(float("-inf")), SchCoord(float("-inf")))
        
        for element in elements:
            bbox = element.get_bounding_box()
        
            point1 = bbox[0]
            point2 = bbox[1]
            
            min_x = min(point1.x, point2.x)
            max_x = max(point1.x, point2.x)
            min_y = min(point1.y, point2.y)
            max_y = max(point1.y, point2.y)
            
            min_point.x = min(min_point.x, min_x)
            min_point.y = min(min_point.y, min_y)
            max_point.x = max(max_point.x, max_x)
            max_point.y = max(max_point.y, max_y)
        
        bbox_width = float(max_point.x - min_point.x) + margin * 2
        bbox_height = float(max_point.y - min_point.y) + margin * 2
                
        bbox_width = max(margin, bbox_width)
        bbox_height = max(margin, bbox_height) 
        
        zoom = min(target_width / bbox_width, target_height / bbox_height)
        
        offset_x = (target_width - bbox_width * zoom) / 2 - float(min_point.x) * zoom
        offset_y = (target_height - bbox_height * zoom) / 2 - float(min_point.y) * zoom
    
        offset_x += margin * zoom
        offset_y += margin * zoom
        
        # print("Autozoom")
        # print(f"BoundingBox: {min_point}; {max_point}")
        # print(f"BoundingBox Size: {bbox_width}; {bbox_height}")
        # print(f"Offset: {offset_x}; {offset_y}")
        
        return SchCoordPoint(SchCoord(offset_x), SchCoord(offset_y)), zoom





        
        

                
# =============================================================================
#     Internal content reading related functions
# =============================================================================   
 
# TODO: Read PinFrac
# TODO: Read PinSymbolLineWidth
# TODO: Read PinWideText
# TODO: Read PinTextData
 
        
    def _CreateRecord(self, record):
        
        RecordId = next((v for k, v in record.items() if k.lower() == "record"), None)
        if RecordId is None:
            raise ValueError("No 'recordid' found.")
                
        if int(RecordId) == 1:
            self.Records.append( SchComponent(record) )
            
        elif int(RecordId) == 2:
            self.Records.append( SchPin(record) )

        elif int(RecordId) == 4:
            self.Records.append( SchLabel(record) )  

        elif int(RecordId) == 5:
            self.Records.append( SchBezier(record) )  
            
        elif int(RecordId) == 6:
            self.Records.append( SchPolyline(record) )    

        elif int(RecordId) == 7:
            self.Records.append( SchPolygon(record) )   

        elif int(RecordId) == 8:
            self.Records.append( SchEllipse(record) ) 
            
        elif int(RecordId) == 11:
            self.Records.append( SchEllipticalArc(record) )   
            
        elif int(RecordId) == 12:
            self.Records.append( SchArc(record) )            

        elif int(RecordId) == 13:
            self.Records.append( SchLine(record) ) 
            
        elif int(RecordId) == 14:
            self.Records.append( SchRectangle(record) )

        elif int(RecordId) == 34:
            self.Records.append( SchDesignator(record) )
            
        elif int(RecordId) == 41:
            self.Records.append( SchParameter(record) )

        elif int(RecordId) == 44:
            self.Records.append( SchImplementationList(record) )
            
        else:
             print(f"Unsupported record id value: {RecordId}")
        

    def _ReadSymbolData(self):
        
        olestream = self._parent._OpenStream(self.Name,  "data")
            
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
                self._CreateRecord( Record() )
                

                

                

        
                
        
                   
                
        
            
