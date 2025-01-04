"""
Schematic Pin Record


"""


from pyaltiumlib.schlib.records.base import (
    _SchCommonParam, _SchLineWidth, _SchCoord
    )


class SchEllipse(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 8 ):
            raise TypeError("Incorrect assigned schematic record")
            
        self.transparent = bool( self.rawdata.get("transparent", "F").upper() == "T" )
        self.issolid = bool( self.rawdata.get("issolid", "F").upper() == "T" )
        self.linewidth = _SchLineWidth(self.rawdata.get('linewidth', 0))              
            
        self.radius = _SchCoord("radius", self.rawdata)           
        self.radius_secondary = _SchCoord("secondaryradius", self.rawdata)    
        
    def __repr__(self):
        return f"SchEllipse "        
        

        
    



