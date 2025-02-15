from pyaltiumlib.datatypes import BinaryReader

# Set up logging
import logging
logger = logging.getLogger(__name__)

class ParameterCollection:
    """
    A class representing a collection of parameters parsed from a string. The collection is shown as
    dictionary or list of dictionaries if multiple records are included.

    :param bytes, optional data: Binary data containing parameters, defaults to None leads an empty class.
    """    
    def __init__(self, data = None):

        self.num_blocks = 0
        self.collection = []
        
        if data:
            self.parse( data )
        else:
            self.data = None

        
    @classmethod
    def from_block(cls, olestream, sizelength=4):
        """
        Alternate constructor to create a ParameterCollection from a block.
        Parses an OLE stream block containing a parameter collection.

        :param olestream olestream: The input binary stream.
        :param int, optional sizelength: Number of bytes indicating the block size, defaults to 4.
        
        :raises ValueError: If stream length does not match expected block length.
        :return: An instance of ParameterCollection.
        :rtype: ParameterCollection
        """
        length = int.from_bytes( olestream.read( sizelength ), "little" )
        
        data = olestream.read( length )
        
        if len(data) != length:
            logger.error("Stream does not match the declared block length.")
                
        return cls( data )


    def __call__(self):
        """
        Returns the parameters stored in the collection.

        :return: The parsed parameter collection.
        :rtype: dict or list
        """
        return  self.collection[0] if self.num_blocks == 1 else self.collection
 
    
    def get_record(self):
        """
        Retrieves the record ID stored in the collection.

        :return: The record ID, or None if not found.
        :rtype: int or None
        """
        if self.num_blocks == 1:
            return self.get("record", None)
            
        return None

       
    def get(self, keys, default=None):
        """
        Retrieves values corresponding to the given keys.

        :param str or list keys: A key or list of keys to search in the collection. 
        :param  any, optional default: The value to return if the key is not found, defaults to None.
        
        :return: The requested values, either as a dict, list, or string.
        :rtype: dict | list | str
        """
        if isinstance(keys, str):
            keys = [keys]
        
        if not isinstance(keys, list):
            logger.error("The `keys` argument must be a string or a list of strings.")

        keys = [key.lower() for key in keys]
        result = {}
        
        for key in keys:
            values = []
            
            for record in self.collection:
                lower_record = {k.lower(): v for k, v in record.items()}
                if key in lower_record:
                    values.append(lower_record[key])
                    
            if values:
                result[key] = values if len(values) > 1 else values[0]
            else:
                result[key] = default
                logger.debug(f"Key '{key}' not found in collection, returning default.")
                
        return result if len(keys) > 1 else result.get(keys[0], default)   


    def get_bool(self, key, default=False):
        """
        Retrieves the value corresponding to the given key as a boolean.

        :param str key: The key to search for in the collection.

        :return: The corresponding boolean value.
        :rtype: bool
        """
        value = self.get( key, None)
        
        if isinstance(value, list):
            logger.error("The `keys` argument must be a string.")
                
        if isinstance(value, str):
            value = value.strip().upper()
            if value == "T":
                return True
            elif value == "TRUE":
                return True
            else:
                return default
            
        else:
            return default

    def get_int(self, key, default=0):
        """
        Retrieves the value corresponding to the given key as a int.

        :param str key: The key to search for in the collection.

        :return: The corresponding boolean value.
        :rtype: bool
        """
        value = self.get( key, None)
        
        if isinstance(value, list):
            logger.error("The `keys` argument must be a string.")
                
        if isinstance(value, str):
            return int(value)

        if isinstance(value, int, float):
            return int(value)            
        else:
            return default            
            
            
    def parse(self, data):
        """
        Parses a block containing parameters separated by '|', where each entry is terminated with 0x00.
        The encoding used is primarily Windows-1252 / ANSI.

        :param bytes data: The binary data containing parameters.

        :raises ValueError: If decoding fails, if the data does not end with 0x00,
                            or if duplicate keys are found in a record.
        """     
                
        if len( data ) == 0:
            logger.warning("Received empty data block.")
            return 
        
        if isinstance(data, bytes):
            try:
                decoded_data = data.decode('windows-1252')
            except UnicodeDecodeError as e:
                logger.error(f"Failed to decode data using Windows-1252 encoding: {e}")
        else:
            decoded_data = data 
    
        if not decoded_data.endswith("\x00"):
            logger.error("Data does not end with 0x00.")
            
        # Split by "RECORD" to handle separate record blocks, otherwise not
        decoded_data = decoded_data.rstrip("\x00")
        if "|RECORD" in decoded_data:
            blocks = [f"|RECORD{block}" for block in decoded_data.strip().split("|RECORD") if block]
        else:
            blocks = [decoded_data.strip()]
    
        self.num_blocks = len(blocks)

        for block in blocks:
            record = {}
            for entry in block.split("|"):
                if "=" in entry:
                    key, value = entry.split("=", 1)
                    if key in record:
                        logger.error(f"Invalid data: Duplicate key '{key}' found in record!")
                        
                    record[key] = value
                    
            if len(record):
                self.collection.append(record)
            
        if len(self.collection) != self.num_blocks:
            logger.error("Invalid data: Length of parameter collection not as expected!")
            
class SchematicPin(ParameterCollection):
    """
    A class representing a collection of parameters parsed from binary data. This class is
    a derivate of the original parameter collection to cover schematic pins

    :param bytes, optional data: Binary data containing parameters, defaults to None leads an empty class.
    """     
    def __init__(self, data = None):
        super().__init__(data)

                
    def parse(self, binary_data):
        """
        Parses a binary data using a binaryReader

        :param bytes data: The binary data containing parameters.

        :raises ValueError: If decoding fails, if the data does not end with 0x00,
                            or if duplicate keys are found in a record.
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