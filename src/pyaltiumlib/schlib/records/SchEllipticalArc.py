"""
Schematic Pin Record


"""


from pyaltiumlib.schlib.records.base import (
    _SchCommonParam, _SchCoord, _SchLineWidth
    )

class SchEllipticalArc(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 11 ):
            raise TypeError("Incorrect assigned schematic record")
            
        self.radius = _SchCoord("radius", self.rawdata)
        self.angle_start = float( self.rawdata.get('startangle', 0) )            
        self.angle_end = float( self.rawdata.get('endangle', 0) )             
        self.linewidth = _SchLineWidth(self.rawdata.get('linewidth', 0))             
            
        
    def __repr__(self):
        return f"SchEllipticalArc "        
        

        
    



