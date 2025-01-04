"""
Schematic Pin Record


"""


from pyaltiumlib.schlib.records.base import _SchCommonParam


class SchDesignator(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 34 ):
            raise TypeError("Incorrect assigned schematic record")
            
            
            
        
    def __repr__(self):
        return f"SchDesignator "        
        

        
    



