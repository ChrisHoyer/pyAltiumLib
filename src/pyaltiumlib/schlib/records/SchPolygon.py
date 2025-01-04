"""
Schematic Pin Record


"""


from pyaltiumlib.schlib.records.base import (
    _SchCommonParam, _SchCoordPoint, _SchCoord, _SchLineWidth)
class SchPolygon(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 7 ):
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
             
            
            
    def __repr__(self):
        return f"SchPolygon "        
        

        
    



