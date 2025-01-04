"""
Schematic Pin Record


"""


from pyaltiumlib.schlib.records.base import _SchCommonParam


class SchParameter(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 41 ):
            raise TypeError("Incorrect assigned schematic record")
            
            
            
        
    def __repr__(self):
        return f"SchParameter "        
        

        
    



