from pyaltiumlib.base import GenericLibFile
from pyaltiumlib.datatypes import ParameterCollection, ParameterColor, ParameterFont
from pyaltiumlib.schlib.symbol import SchLibSymbol

# Set up logging
import logging
logger = logging.getLogger(__name__)

class SchLib(GenericLibFile):
    """
    Schematic class for handling Altium Designer schematic library files.
    During initialization the library file will be read.
    
    :param string filepath: The path to the .SchLib library file
    :param io.BytesIO oleobj: A file-like object containing the altium library file binary stream
    
    :raises FileNotFoundError: If file is not a supported file.
    :raises ValueError: If library data or header can not be read
    """
    
    def __init__(self, filepath, oleobj):
        super().__init__(filepath, oleobj)
        
        self.LibType = "Schematic"
        
        # Implement System Font
        self._SystemFontID = 0
        self._Fonts = []
        self._Fonts.append( ParameterFont("Times New Roman", 10) )
        
        self._ReadSchematicLibrary()
        
        self.OleObj.close()
        logger.info(f"Reading and extracting of '{self.FileName}' done.")
        

# =============================================================================
#     Internal content reading related functions
# =============================================================================   
        
    def _ReadSchematicLibrary(self) -> None:
        try:
            self._ReadSchematicFileHeader()
            self._ReadSchematicLibraryData()
            
        except Exception as e:
            logger.error(f"Failed to read library: {e}")
            raise
            

    def _ReadSchematicFileHeader(self) -> None:
        
        self._FileHeader = ParameterCollection.from_block( self._OpenStream("",  "FileHeader")  )
        self.LibHeader = self._FileHeader.get("header", "")
        
        logger.debug(f" Fileheader of library file '{self.FileName}' is '{self.LibHeader}'.")
        if "Schematic" in self.LibHeader and "Binary File" in self.LibHeader:
            logger.info(f"File '{self.FileName}' identified as schematic binary library file.")
        else:
            logger.warning(f"File '{self.FilePath}' can not be identified as schematic binary library!")
    
        # Extract Fonts  (1....FontCount)
        self._FontCount = int( self._FileHeader.get("fontidcount"), 0)
        logger.debug(f"Start extracting {self._FontCount} fonts(s) from '{self.FileName}'.")
        
        for index in range(self._FontCount + 1):
            font = self._FileHeader.get(f'fontname{index}', None)
            size = self._FileHeader.get(f'size{index}', "")
            italic = self._FileHeader.get_bool(f'italic{index}')
            bold = self._FileHeader.get_bool(f'bold{index}')
            underline = self._FileHeader.get_bool(f'underline{index}')
            strikeout = self._FileHeader.get_bool(f'strikeout{index}')
            
            if font:
                self._Fonts.append( ParameterFont( font, size, bold, italic, underline, strikeout ))
        
        # Generic parameter
        self._BackgroundColor = ParameterColor(self._FileHeader.get('areacolor', 16317695))       

            
    def _ReadSchematicLibraryData(self):
                                             
        # Extract and Read Components (0....CompCount)
        self.ComponentCount = int( self._FileHeader.get("compcount"), 0) 
        logger.info(f"Start extracting {self.ComponentCount} component(s) from '{self.FileName}'.")
        
        for index in range(self.ComponentCount):
            lib_ref = self._FileHeader.get(f'LibRef{index}', None)
            descr = self._FileHeader.get(f'CompDescr{index}', "")  
            parts = self._FileHeader.get(f'PartCount{index}', "") 
            
            if lib_ref:
                self.Parts.append( SchLibSymbol( self, lib_ref, 
                                                description = descr,
                                                partcount = parts ) )
                      