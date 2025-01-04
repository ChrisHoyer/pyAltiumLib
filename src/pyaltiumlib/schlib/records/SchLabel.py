"""
Schematic Pin Record


"""


from pyaltiumlib.schlib.records.base import (
    _SchCommonParam, _SchTextOrientation, _SchTextJustification
    )


class SchLabel(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 4 ):
            raise TypeError("Incorrect assigned schematic record")
            

        self.orientation = _SchTextOrientation( self.rawdata.get("orientation", 0))
        self.justification = _SchTextJustification( self.rawdata.get("justification", 0))
        
        self.font_id = int(self.rawdata.get("fontid", 0))
        self.text = self.rawdata.get("text", "")
        self.is_mirrored = self.rawdata.get("ismirrored", "F").upper() == "T"
        self.is_hidden = self.rawdata.get("ishidden", "F").upper() == "T"
            
            
        
    def __repr__(self):
        return f"SchLabel "        
        

        
    



