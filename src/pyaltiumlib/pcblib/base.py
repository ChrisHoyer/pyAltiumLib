"""



"""

from pyaltiumlib.base import GenericLib

class PcbLib(GenericLib):
    
    def __init__(self, filepath):
        
        super().__init__(filepath)
        
        self.ReadFile()
    

    def ReadFile(self):
        
        self._OpenFile()

        ComponentParamsTOC = self._OpenStream( "Library/ComponentParamsTOC/Data" )
        
        # Read Library TOC   
        Length = int.from_bytes( ComponentParamsTOC.read(4), "little" ) 
        ComponentParamsTOC = self._ParseGenericProperties( ComponentParamsTOC.read(Length), output_blocks=True )
        
        # Transform Library TOC into Pcb Component Class
        for component in ComponentParamsTOC:
            lib_ref = component.get('Name', None)
            comp_descr = component.get('Description', None)
            
            # Only add the part if all 3 keys are found
            if lib_ref and comp_descr:
                print( lib_ref )
            
        self._CloseFile()
        
        
        
        

                    
