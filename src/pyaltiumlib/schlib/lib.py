from pyaltiumlib.base import GenericLibFile
from pyaltiumlib.schlib.symbol import SchLibSymbol
from pyaltiumlib.datatypes import ParameterCollection, ParameterColor, ParameterFont


class SchLib(GenericLibFile):
    
    def __init__(self, filepath):
        super().__init__(filepath)
        
        # Implement System Font
        self.SystemFontID = 0
        self.Fonts = []
        self.Fonts.append( ParameterFont("Times New Roman", 10) )
        
        self._ReadFileHeader()

        
    def _ReadFileHeader(self):
        
        self._OpenFile()

        self._FileHeader = ParameterCollection.from_block( self._OpenStream("",  "FileHeader")  )

        # Extract Fonts  (1....FontCount)
        self.FontCount = int( self._FileHeader.get("fontidcount"), 0)
        for index in range(self.FontCount + 1):
            font = self._FileHeader.get(f'fontname{index}', None)
            size = self._FileHeader.get(f'size{index}', "")
            italic = self._FileHeader.get_bool(f'italic{index}')
            bold = self._FileHeader.get_bool(f'bold{index}')
            underline = self._FileHeader.get_bool(f'underline{index}')
            strikeout = self._FileHeader.get_bool(f'strikeout{index}')
            
            if font:
                self.Fonts.append( ParameterFont( font, size, bold, italic, underline, strikeout ))
        
        # Generic parameter

        self.background = ParameterColor(self._FileHeader.get('areacolor', 16317695))
                
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
  
        self._CloseFile()
        
   

                    
