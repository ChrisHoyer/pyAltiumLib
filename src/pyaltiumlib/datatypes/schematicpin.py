from pyaltiumlib.datatypes import BinaryReader, ParameterCollection

class SchematicPin(ParameterCollection):
    
    def __init__(self, data = None):
        super().__init__(data)

                
    def _parse(self, binary_data):
        """
        Pin Properties as binary record converted to ASCII
        """
        
        record = {}
        data = BinaryReader( binary_data )
    
        record["record"] = data.read_int32()
        data.read_byte() # Unknown
        record["OwnerPartId"] = data.read_int16()   
        record["OwnerPartDisplayMode"] = data.read_int8()   
        record["Symbol_InnerEdge"] = data.read_int8() 
        record["Symbol_OuterEdge"] = data.read_int8() 
        record["Symbol_Inside"]  = data.read_int8() 
        record["Symbol_Outside"] = data.read_int8() 
        record["Symbol_Linewidth"]  = 0 # Not implemented?
        
        entry_length = data.read_int8()   
        data.read_int8() # Why?
        record["Description"] = "" if entry_length == 0 else data.read(entry_length).decode("utf-8") 
        
        record["Electrical_Type"] = data.read_int8() 
        
        # Schematic Pin Flags
        flags = data.read_int8() 
        record["Rotated"] = bool( flags & 0x01 )        
        record["Flipped"] = bool( flags & 0x02 )
        record["Hide"] = bool( flags & 0x04 )
        record["Show_Name"] = bool( flags & 0x08 )  
        record["Show_Designator"] = bool( flags & 0x10 )
        record["Graphically_Locked"] = bool( flags & 0x40 )
    
        record["Length"] = data.read_int16()
        record["Location.X"] = data.read_int16(signed=True)
        record["Location.Y"] = data.read_int16(signed=True)
        
        record["Color"] = data.read_int32()

        entry_length = data.read_int8() 
        record["Name"] = "" if entry_length == 0 else data.read(entry_length).decode("utf-8") 

        entry_length = data.read_int8() 
        record["Designator"] = "" if entry_length == 0 else data.read(entry_length).decode("utf-8")
                                
        self.num_blocks = 1
        self.collection.append(record) 