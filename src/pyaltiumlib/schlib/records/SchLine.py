"""
Schematic Pin Record


"""


from pyaltiumlib.schlib.records.base import (
    _SchCommonParam, _SchLineWidth, _SchLineStyle, 
    _SchCoordPoint, _SchCoord
    )


class SchLine(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 13 ):
            raise TypeError("Incorrect assigned schematic record")
            
        self.linewidth = _SchLineWidth(self.rawdata.get('linewidth', 0))             
        self.linestyle = _SchLineStyle(self.rawdata.get('linestyle', 0)) 
        
        self.corner = _SchCoordPoint(_SchCoord("corner.x", self.rawdata),
                                     _SchCoord("corner.y", self.rawdata))           
        
    def __repr__(self):
        return f"SchLine "        
        

        
    



