"""



"""

import os
import olefile

class AltiumLib:
 
    def __init__(self, filepath):
        
        self.filepath = filepath
        self._olefile = None 
        self._olefile_open = False

        if not olefile.isOleFile( filepath ): 
            raise FileNotFoundError(f"{filepath} is not a supported OLE file.")
            
        # extracted file content
        self.parts = []

# =============================================================================
#     External access 
# =============================================================================
    
    def list_parts(self):
        return [x.name for x in self.parts]


# =============================================================================
#     Internal file handling related functions
# =============================================================================

    def _OpenFile(self):
        
        if self._olefile_open:
            raise ValueError(f"file: { self.filepath }. Already open!")
                
        try:
            self._olefile = olefile.OleFileIO( self.filepath )
            self._olefile_open = True
        except Exception as e:
            raise ValueError(f"Failed to open file: { self.filepath }. Error: {e}")


    def _OpenStream(self, container, stream):
                
        if not self._olefile_open:
            raise ValueError(f"file: { self.filepath }. File not open!")
                    
        if not container == "":
            
            if not self._olefile.exists( container ):
                raise ValueError(f"Part '{container}' does not exist in file '{self.filepath}'!")
                
            illegal_characters = '<>:"/\\|?*\x00'
            container = "".join("_" if char in illegal_characters else char for char in container)
            
        return self._olefile.openstream( f"{container}/{stream}" if container else stream )


    def _CloseFile(self):
        if hasattr(self, '_olefile') and self._olefile is not None:
            self._olefile.close()
            self._olefile_open = False
            

# =============================================================================
#     Internal data reading related functions
# =============================================================================   
 
    def _ReadBlock(self, olestream):
        """
        Represents a data structure containing the length of the block and the data.
        The first 4 bytes define the length of the block (little-endian).
        """        

        length = int.from_bytes( olestream.read(4), "little" )
        
        data = olestream.read( length )
        
        if len(data) != length:
            raise ValueError("Stream does not match the declared block length.")        
        
        return length, data
   
        
    def _ParseParameterCollection(self, data, output_blocks=False):
        """
        Parses a block containing separated parameters as data, each 0x00 terminated.
        The encoding used is mostly Windows-1252 / ANSI.
    
        Each parameter in the collection is separated using '|'.
        The key and value of each parameter are separated by '='.
        Parameter keys can appear
        """       
                
        if len( data ) == 0:
            raise ValueError("Data does not match the declared block length.")    
        
        try:
           decoded_data = data.decode('windows-1252')
           
        except UnicodeDecodeError as e:
               raise ValueError("Failed to decode data using Windows-1252 encoding.") from e      

        if not decoded_data.endswith("\x00"):
            raise ValueError("Data does not end with 0x00.")
            
        # Split by line breaks to handle separate blocks
        blocks = decoded_data[:-1].split("\n")
        collection = []

        for block in blocks:
            record = {}
            for entry in block.split("|"):
                if "=" in entry:
                    key, value = entry.split("=", 1)
                    if key in record:
                        raise ValueError("Invalid data. Record {key} already exists!")
                    record[key] = value

            collection.append(record)
            
        # TODO: check if blocks are requested
        if output_blocks and (len(collection) == 1):
                raise ValueError("Invalid data. Block output for parsing properties expected!")
        else:
            collection = collection[0]
            
        return collection


    def _ParseSchematicPin(self, data):
        """
        Pin Properties as binary record converted to ASCII
        """
        
        cursor_offset = 0
    
        record = {}
        record["Record"] = int.from_bytes( data[0:3], "little" )
        
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
        
        return record  


