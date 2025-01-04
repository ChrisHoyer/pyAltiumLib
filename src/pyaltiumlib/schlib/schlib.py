"""



"""

from pyaltiumlib.base import AltiumLib
from pyaltiumlib.schlib.symbol import SchLibSymbol

class SchLib(AltiumLib):
    
    def __init__(self, filepath):
        
        super().__init__(filepath)
        
        self._ReadFileHeader()
    

# =============================================================================
#     Internal content reading related functions
# =============================================================================   

    def _ReadFileHeader(self):
        
        self._OpenFile()

        _, data = self._ReadBlock( self._OpenStream("",  "FileHeader") )
        
        self.FileHeader = self._ParseParameterCollection( data )
           
                    
        # Transform File Header into SchLib Component Class
        index = 0
        while f'LibRef{index}' in self.FileHeader:
            
            lib_ref = self.FileHeader.get(f'LibRef{index}', None)
            descr = self.FileHeader.get(f'CompDescr{index}', "")  
            parts = self.FileHeader.get(f'PartCount{index}', "")              
            
            self.parts.append( SchLibSymbol(self, lib_ref, 
                                             description = descr,
                                             partcount = parts ) )
         
            index += 1
            
        self._CloseFile()

    

                    
