"""



"""
import json

from pyaltiumlib.base import GenericLibFile
from pyaltiumlib.schlib.symbol import SchLibSymbol
from pyaltiumlib.datatypes import ParameterCollection


class SchLib(GenericLibFile):
    
    def __init__(self, filepath):
        
        super().__init__(filepath)
        
        self._ReadFileHeader()

        
    def _ReadFileHeader(self):
        
        self._OpenFile()

        self._FileHeader = ParameterCollection.from_block( self._OpenStream("",  "FileHeader")  )
                 
        self.ComponentCount = int( self._FileHeader.get("compcount"), 0) 
        for index in range(self.ComponentCount):
            
            lib_ref = self._FileHeader.get(f'LibRef{index}', None)
            descr = self._FileHeader.get(f'CompDescr{index}', "")  
            parts = self._FileHeader.get(f'PartCount{index}', "")              
            
            if lib_ref:
                symbol = SchLibSymbol( self, 
                                       lib_ref,
                                       description = descr,
                                       partcount = parts )
                
                self.Parts.append( symbol )
            
        self._CloseFile()
        
   

                    
