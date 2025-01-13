"""



"""

import json
import olefile

class GenericLibFile:
 
    def __init__(self, filepath):

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


    def __repr__(self):
        return self.toJSON()
    
# =============================================================================
#     External access 
# =============================================================================
 
    def ListParts(self):
        return [x.Name for x in self.Parts]


    def GetPart(self, name):
            for part in self.Parts:
                if part.Name == name:
                    return part
            return None
    

    def toJSON(self):
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

    def _OpenFile(self):
        
        if self._olefile_open:
            raise ValueError(f"file: { self.FilePath }. Already open!")
                
        try:
            self._olefile = olefile.OleFileIO( self.FilePath )
            self._olefile_open = True
        except Exception as e:
            raise ValueError(f"Failed to open file: { self.FilePath }. Error: {e}")


    def _OpenStream(self, container, stream):
                
        if not self._olefile_open:
            raise ValueError(f"file: { self.FilePath }. File not open!")
                    
        if not container == "":

            illegal_characters = '<>:"/\\|?*\x00'
            container = "".join("_" if char in illegal_characters else char for char in container)
            
            if not self._olefile.exists( container ):
                raise ValueError(f"Part '{container}' does not exist in file '{self.FilePath}'!")
       
        return self._olefile.openstream( f"{container}/{stream}" if container else stream )


    def _CloseFile(self):
        if hasattr(self, '_olefile') and self._olefile is not None:
            self._olefile.close()
            self._olefile_open = False

