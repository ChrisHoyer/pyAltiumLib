from pyaltiumlib.datatypes import ParameterColor

import json
import olefile
import logging
from typing import List, Optional, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenericLibFile:
    """
    A base class for handling generic library files in Altium format.

    Attributes:
        LibType (type): The type of the library.
        LibHeader (str): The header of the library.
        FilePath (str): The path to the library file.
        ComponentCount (int): The number of components in the library.
        Parts (List[Any]): A list of parts in the library.
        _BackgroundColor (ParameterColor): The background color of the library.
    """ 
    
    def __init__(self, filepath: str):
        """
        Initialize a GenericLibFile object.

        Args:
            filepath (str): The path to the library file.
        """
        if not olefile.isOleFile( filepath ): 
            raise FileNotFoundError(f"{filepath} is not a supported OLE file.")
            
        self.LibType = type(self)
        self.LibHeader = ""
        
        self.FilePath = filepath        
        self._olefile = None
        self._olefile_open = False
         
        # extracted file content
        self._FileHeader = None
        self.ComponentCount = 0
        self.Parts = []
        
        self._BackgroundColor = ParameterColor.from_hex("#6D6A69")  


    def __repr__(self) -> str:
        """
        Return a JSON representation of the public attributes of the object.

        Returns:
            str: A JSON string representation of the object.
        """
        return self.toJSON()
    
# =============================================================================
#     External access 
# =============================================================================
 
    def ListParts(self) -> List[str]:
        """
        List the names of all parts in the library.

        Returns:
            List[str]: A list of part names.
        """
        return [x.Name for x in self.Parts]


    def GetPart(self, name: str) -> Optional[Any]:
        """
        Get a part by its name.

        Args:
            name (str): The name of the part.

        Returns:
            Optional[Any]: The part object if found, otherwise None.
        """
        for part in self.Parts:
            if part.Name == name:
                return part
        return None
    

    def toJSON(self) -> str:
        """
        Converts public attributes of the high level file to a JSON-compatible dictionary.
    
        Returns:
            str: A JSON string representation of the public instance attributes.
        """
        public_attributes = {
            key: value if isinstance(value, str) else str(value)
            for key, value in self.__dict__.items()
            if not key.startswith("_")
            }
        
        for key, value in public_attributes.items():
            try:
                if isinstance(value, str):
                    json.loads(value)
            except (json.JSONDecodeError, TypeError):
                pass
            
            else:
                public_attributes[key] = json.loads(value)
    
        return json.dumps(public_attributes, indent=4)

# =============================================================================
#     Internal file handling related functions
# =============================================================================

    def _OpenFile(self) -> None:
        """
        Open the library file for reading.
        """        
        if self._olefile_open:
            raise ValueError(f"file: { self.FilePath }. Already open!")
                
        try:
            self._olefile = olefile.OleFileIO( self.FilePath )
            self._olefile_open = True
        except Exception as e:
            logger.error(f"Failed to open file: {self.FilePath}. Error: {e}")
            raise

    def _OpenStream(self, container: str, stream: str) -> Any:
        """
        Open a stream within the library file.

        Args:
            container (str): The container name.
            stream (str): The stream name.

        Returns:
            Any: The opened stream.
        """                
        if not self._olefile_open:
            logger.error(f"file: { self.FilePath }. File not open!")
            raise
                    
        if not container == "":

            illegal_characters = '<>:"/\\|?*\x00'
            container = "".join("_" if char in illegal_characters else char for char in container)
            
            if not self._olefile.exists( container ):
                logger.error(f"Part '{container}' does not exist in file '{self.FilePath}'!")
                raise
        
        return self._olefile.openstream( f"{container}/{stream}" if container else stream )


    def _CloseFile(self) -> None:
        """
        Close the library file.
        """
        if hasattr(self, '_olefile') and self._olefile is not None:
            self._olefile.close()
            self._olefile_open = False

