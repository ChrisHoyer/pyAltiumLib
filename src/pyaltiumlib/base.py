from pyaltiumlib.datatypes import ParameterColor

import os
import olefile
from typing import List, Optional, Dict, Any

# Set up logging
import logging
logger = logging.getLogger(__name__)

class GenericLibFile:
    """
    Base class for handling Altium Designer library files.

    This class provides fundamental functionality for reading library files
    in Altium Designer format.
    
    :param io.BytesIO oleobj: A file-like object containing the altium library file binary stream
    
    :raises FileNotFoundError: If file is not a supported file.
    """  
    
    def __init__(self, filepath: str, oleobj):

            
        self.LibType = type(self) 
        """
        `string` that specifies the type of the library.
        """
        
        self.LibHeader = ""
        """
        `string` that stores the header information of the library.
        """
                
        self.FilePath = filepath 
        """
        `string` that contains the file path to the library.
        """
        
        self.FileName = os.path.basename(filepath)
        """
        `string` that contains the name of the library.
        """

        self.ComponentCount = 0
        """
        `int` with total number of components in the library.
        """
        
        self.Parts = []
        """
        `List[any]` is a collection of components derived from :class:`pyaltiumlib.libcomponent.LibComponent` in their specific class 
        contained in the library.
        """ 
        
        self.OleObj = oleobj
         
        # extracted file content
        self._FileHeader = None
        
        self._BackgroundColor = ParameterColor.from_hex("#6D6A69")  


    def __repr__(self) -> str:
        """
        Converts public attributes of the high level file to a string.

        :return: A string representation of the content of the object
        :rtype: str
        """
        return str( self.read_meta() )
    
# =============================================================================
#     External access 
# =============================================================================
    
    def read_meta(self) -> Dict:
        """
        Converts public attributes of the high level file to a dictionary.

        :return: A dict representation of the content of the object
        :rtype: Dict
        """
        public_attributes = {
            key: value if isinstance(value, str) else str(value)
            for key, value in self.__dict__.items()
            if not key.startswith("_")
            }
        return public_attributes        
 
        
    def list_parts(self) -> List[str]:
        """
        List the names of all parts in the library.

        :return: A list of part names
        :rtype: List[str]
        """
        return [x.Name for x in self.Parts]

    
    def get_part(self, name: str) -> Optional[Any]:
        """
        Get a part of the library by its name.
        
        :param string name: The name of the part.

        :return: The part class derived from :class:`pyaltiumlib.libcomponent.LibComponent` if found, otherwise None.
        :rtype: Optional[Any]
        """
        for part in self.Parts:
            if part.Name == name:
                return part
            
        raise KeyError(f"Part '{name}' not found in '{self.FileName}'.")
    

# =============================================================================
#     Internal file handling related functions
# =============================================================================

    def _OpenStream(self, container: str, stream: str) -> Any:
        """
        Open a stream within the library file.

        Args:
            container (str): The container name.
            stream (str): The stream name.

        Returns:
            Any: The opened stream.
        """                

        if not container == "":

            illegal_characters = '<>:"/\\|?*\x00'
            container = "".join("_" if char in illegal_characters else char for char in container)
            container = (container[:31]) if len(container) > 31 else container
            
            if not self.OleObj.exists( container ):
                logger.error(f"Part '{container}' does not exist in file '{self.FilePath}'!")
                raise FileNotFoundError(f"Part '{container}' does not exist in file '{self.FilePath}'!")
        
        return self.OleObj.openstream( f"{container}/{stream}" if container else stream )

