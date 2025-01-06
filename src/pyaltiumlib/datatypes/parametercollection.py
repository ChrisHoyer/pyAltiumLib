"""

"""

from ._utils import ReadBlock

class ParameterCollection:
    
    def __init__(self, data = None):

        self.num_blocks = 0
        self.collection = []
        
        if data:
            self._parse( data )
        else:
            self.data = None

        
    @classmethod
    def from_block(cls, olestream, sizelength=4):
        """
        Alternate constructor to create a ParameterCollection from a block.
        Parses an ole stream block containing a parameter collection
        """ 
        _, data = ReadBlock( olestream,  sizelength=sizelength)
                
        return cls( data )


    def __call__(self):
        """
          Returns:
                dict: The parameters stored in the collection.
        """
        return  self.collection[0] if self.num_blocks == 1 else self.collection
 
       
    def get(self, keys, default=None):
        """
        Retrieves all values corresponding to the given keys.
    
        Args:
            keys (str | list): A key or a list of keys to search for in the collection.
            default (any, optional): The value to return if a key is not found. Defaults to None.
    
        Returns:
            dict | list | str: A dictionary where the key is the requested key and the value
                               is either a single value or a list of values if the key exists
                               in multiple records. If a single key is provided, returns its
                               corresponding values directly or the `default` value if not found.
        """
        if isinstance(keys, str):
            keys = [keys]
        
        if not isinstance(keys, list):
            raise TypeError("The `keys` argument must be a string or a list of strings.")

        keys = [key.lower() for key in keys]
        result = {}
        for key in keys:
            values = []
            for record in self.collection:
                if key in record:
                    values.append(record[key])
            if values:
                result[key] = values if len(values) > 1 else values[0]
            else:
                result[key] = default
                
        return result if len(keys) > 1 else result.get(keys[0], default)   

    
    def _parse(self, data):
        """
        Parses a block containing separated parameters as data, each 0x00 terminated.
        The encoding used is mostly Windows-1252 / ANSI.
    
        Each parameter in the collection is separated using '|'.
        The key and value of each parameter are separated by '='.
        """       
                
        if len( data ) == 0:
            return 
        
        try:
           decoded_data = data.decode('windows-1252')
           
        except UnicodeDecodeError as e:
               raise ValueError("Failed to decode data using Windows-1252 encoding.") from e      
    
        if not decoded_data.endswith("\x00"):
            raise ValueError("Data does not end with 0x00.")
            
        # Split by line breaks to handle separate blocks
        blocks = decoded_data[:-1].split("\n")
        self.num_blocks = len(blocks)

        for block in blocks:
            record = {}
            for entry in block.split("|"):
                if "=" in entry:
                    key, value = entry.split("=", 1)
                    if key.lower() in record:
                        raise ValueError("Invalid data. Record {key} already exists!")
                    record[key.lower()] = value
    
            self.collection.append(record)
            
        if len(self.collection) != self.num_blocks:
            raise ValueError("Invalid data. Length of parameter collection not expected!")
            
