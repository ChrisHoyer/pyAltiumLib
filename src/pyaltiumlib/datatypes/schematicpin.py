"""

"""

from ._utils import ReadBlock

class SchematicPin:
    
    def __init__(self, data = None):

        self.records = {}
        
        if data:
            self._parse( data )
        else:
            self.data = None


    def __call__(self):
        """
          Returns:
                dict: The records stored in a dict.
        """
        return  self.records

    
    def _parse(self, data):
        """
        Pin Properties as binary record converted to ASCII
        """
        
        cursor_offset = 0
    
        self.records["record"] = int.from_bytes( data[0:3], "little" )
        
        self.records["OwnerPartId"] = int.from_bytes( data[5:6], "little" )        
        self.records["OwnerPartDisplayMode"] = data[7]       
        self.records["Symbol_InnerEdge"] = data[8]
        self.records["Symbol_OuterEdge"] = data[9]
        self.records["Symbol_Inside"]  = data[10]
        self.records["Symbol_Outside"] = data[11]
        self.records["Symbol_Linewidth"]  = 0 # Not implemented?
        
        entry_length = data[12 + cursor_offset]
        self.records["Description"] = ""
        
        if entry_length != 0:
            self.records["Description"] = data[13 + cursor_offset: 13 + cursor_offset + entry_length ].decode("utf-8")
            cursor_offset += entry_length
        
        self.records["Electrical_Type"] = data[14 + cursor_offset]
        
        # Schematic Pin Flags
        self.records["Rotated"] = bool( data[15 + cursor_offset] & 0x01 )        
        self.records["Flipped"] = bool( data[15 + cursor_offset] & 0x02 )
        self.records["Hide"] = bool( data[15 + cursor_offset] & 0x04 )
        self.records["Show_Name"] = bool( data[15 + cursor_offset] & 0x08 )  
        self.records["Show_Designator"] = bool( data[15 + cursor_offset] & 0x10 )
        self.records["Graphically_Locked"] = bool( data[15 + cursor_offset] & 0x40 )
    
        self.records["Length"] = int.from_bytes( data[16 + cursor_offset:17 + cursor_offset], "little")
        self.records["Location.X"] = int.from_bytes( data[18 + cursor_offset:19 + cursor_offset], "little", signed=True)
        self.records["Location.Y"] = int.from_bytes( data[20 + cursor_offset:21 + cursor_offset], "little", signed=True)
        
        self.records["Color"] = int.from_bytes( data[22 + cursor_offset:25 + cursor_offset], "little")
    
        entry_length = data[26 + cursor_offset]
        self.records["Name"] = ""
        if entry_length != 0:
            self.records["Name"] = data[27 + cursor_offset: 27 + cursor_offset + entry_length ].decode("utf-8")
            cursor_offset += entry_length
    
        entry_length = data[27 + cursor_offset]
        self.records["Designator"] = ""
        if entry_length != 0:
            self.records["Designator"] = data[28 + cursor_offset: 28 + cursor_offset + entry_length ].decode("utf-8")
            cursor_offset += entry_length
