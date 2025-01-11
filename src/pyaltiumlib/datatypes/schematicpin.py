"""

"""
from .parametercollection import ParameterCollection

class SchematicPin(ParameterCollection):
    
    def __init__(self, data = None):
        super().__init__(data)

                
    def _parse(self, data):
        """
        Pin Properties as binary record converted to ASCII
        """
        
        record = {}
        cursor_offset = 0
    
        record["record"] = int.from_bytes( data[0:3], "little" )
        
        record["OwnerPartId"] = int.from_bytes( data[5:6], "little" )        
        record["OwnerPartDisplayMode"] = data[7]       
        record["Symbol_InnerEdge"] = data[8]
        record["Symbol_OuterEdge"] = data[9]
        record["Symbol_Inside"]  = data[10]
        record["Symbol_Outside"] = data[11]
        record["Symbol_Linewidth"]  = 0 # Not implemented?
        
        entry_length = data[12 + cursor_offset]
        record["Description"] = ""
        
        if entry_length != 0:
            record["Description"] = data[13 + cursor_offset: 13 + cursor_offset + entry_length ].decode("utf-8")
            cursor_offset += entry_length
        
        record["Electrical_Type"] = data[14 + cursor_offset]
        
        # Schematic Pin Flags
        record["Rotated"] = bool( data[15 + cursor_offset] & 0x01 )        
        record["Flipped"] = bool( data[15 + cursor_offset] & 0x02 )
        record["Hide"] = bool( data[15 + cursor_offset] & 0x04 )
        record["Show_Name"] = bool( data[15 + cursor_offset] & 0x08 )  
        record["Show_Designator"] = bool( data[15 + cursor_offset] & 0x10 )
        record["Graphically_Locked"] = bool( data[15 + cursor_offset] & 0x40 )
    
        record["Length"] = int.from_bytes( data[16 + cursor_offset:17 + cursor_offset], "little")
        record["Location.X"] = int.from_bytes( data[18 + cursor_offset:19 + cursor_offset], "little", signed=True)
        record["Location.Y"] = int.from_bytes( data[20 + cursor_offset:21 + cursor_offset], "little", signed=True)
        
        record["Color"] = int.from_bytes( data[22 + cursor_offset:25 + cursor_offset], "little")
    
        entry_length = data[26 + cursor_offset]
        record["Name"] = ""
        if entry_length != 0:
            record["Name"] = data[27 + cursor_offset: 27 + cursor_offset + entry_length ].decode("utf-8")
            cursor_offset += entry_length
    
        entry_length = data[27 + cursor_offset]
        record["Designator"] = ""
        if entry_length != 0:
            record["Designator"] = data[28 + cursor_offset: 28 + cursor_offset + entry_length ].decode("utf-8")
            cursor_offset += entry_length
                        
        self.num_blocks = 1
        self.collection.append(record)
