"""
Schematic Pin Record


"""


from pyaltiumlib.schlib.records.base import (
    _SchCommonParam, _SchLineWidth,  _SchCoordPoint, _SchCoord
    )

class SchRectangle(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 14 ):
            raise TypeError("Incorrect assigned schematic record")
            
        self.linewidth = _SchLineWidth(self.rawdata.get('linewidth', 0))             
        self.transparent = bool( self.rawdata.get("transparent", "F").upper() == "T" )
        self.issolid = bool( self.rawdata.get("issolid", "F").upper() == "T" )
        
        self.corner =  _SchCoordPoint(_SchCoord("corner.x", self.rawdata),
                                      _SchCoord("corner.y", self.rawdata))               
            
        
    def __repr__(self):
        return f"SchRectangle "        
        

        
    



