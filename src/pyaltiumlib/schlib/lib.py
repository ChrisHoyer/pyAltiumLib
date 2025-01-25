from pyaltiumlib.base import GenericLibFile
from pyaltiumlib.datatypes import ParameterCollection, ParameterColor, ParameterFont
from pyaltiumlib.schlib.symbol import SchLibSymbol
from typing import List, Optional, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SchLib(GenericLibFile):
    """
    A class to handle Altium Schematic Library files (.SchLib).
    
    Attributes:
        LibType (str): The type of library (e.g., "Schematic").
        _SystemFontID (int): The ID of the system font.
        _Fonts (List[ParameterFont]): A list of fonts used in the library.
        _FontCount (int): The number of fonts in the library.
    """    
    
    def __init__(self, filepath: str):
        """
        Initialize a SchLib object.

        Args:
            filepath (str): The path to the .SchLib file.
        """
        super().__init__(filepath)
        
        self.LibType = "Schematic"
        
        # Implement System Font
        self._SystemFontID = 0
        self._Fonts = []
        self._Fonts.append( ParameterFont("Times New Roman", 10) )
        
        self._ReadLibrary()

        
    def _ReadLibrary(self) -> None:
        """
        Read the library file and extract its contents.
        """
        try:
            self._OpenFile()
            self._ReadFileHeader()
        except Exception as e:
            logger.error(f"Failed to read library: {e}")
            raise
        finally:
            self._CloseFile()
        

    def _ReadFileHeader(self) -> None:
        """
        Read the file header and extract metadata, fonts, and components.
        """
        try:
        
            self._FileHeader = ParameterCollection.from_block( self._OpenStream("",  "FileHeader")  )
        
            self.LibHeader = self._FileHeader.get("header", "")
        
            # Extract Fonts  (1....FontCount)
            self._FontCount = int( self._FileHeader.get("fontidcount"), 0)
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
                                             
            # Extract and Read Components (0....CompCount)
            self.ComponentCount = int( self._FileHeader.get("compcount"), 0) 
            for index in range(self.ComponentCount):
                lib_ref = self._FileHeader.get(f'LibRef{index}', None)
                descr = self._FileHeader.get(f'CompDescr{index}', "")  
                parts = self._FileHeader.get(f'PartCount{index}', "") 
                
                if lib_ref:
                    self.Parts.append( SchLibSymbol( self, lib_ref, 
                                                    description = descr,
                                                    partcount = parts ) )
        except Exception as e:
            logger.error(f"Failed to read file header: {e}")
            raise                       