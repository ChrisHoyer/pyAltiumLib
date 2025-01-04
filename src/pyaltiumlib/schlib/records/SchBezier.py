"""
Schematic Pin Record


"""


from pyaltiumlib.schlib.records.base import (
    _SchCommonParam, _SchCoordPoint, _SchCoord,
    _SchLineWidth, _SchLineStyle
    )


class SchBezier(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 5 ):
            raise TypeError("Incorrect assigned schematic record")

        self.transparent = bool( self.rawdata.get("transparent", "F").upper() == "T" )
        self.issolid = bool( self.rawdata.get("issolid", "F").upper() == "T" )
        self.linewidth = _SchLineWidth(self.rawdata.get('linewidth', 0))  
            
        self.num_vertices = int( self.rawdata.get('locationcount', 0) )
        
        self.vertices = []
        for i in range(self.num_vertices):
            
            xy = _SchCoordPoint(_SchCoord(f"x{i+1}", self.rawdata),
                                _SchCoord(f"y{i+1}", self.rawdata))
            
            self.vertices.append( xy )
                       
        self.linestyle = _SchLineStyle(self.rawdata.get('linestyle', 0))              
            
        
    def __repr__(self):
        return f"SchBezier "        
        

        
    



