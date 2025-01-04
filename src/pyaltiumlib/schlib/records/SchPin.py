"""
Schematic Pin Record

https://pyaltiumlib.readthedocs.io/latest/fileformat/Primitives_SchLib.html#id-2-pin
"""


from pyaltiumlib.schlib.records.base import (
    _SchCommonParam, _SchPinSymbol, _SchLineWidth,
    _SchPinElectricalType
    )


class SchPin(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 2 ):
            raise TypeError("Incorrect assigned schematic record")
        
        
        self.symbol_inneredge = _SchPinSymbol(self.rawdata.get('symbol_inneredge', 0))
        self.symbol_outeredge = _SchPinSymbol(self.rawdata.get('symbol_outeredge', 0))
        self.symbol_inside = _SchPinSymbol(self.rawdata.get('symbol_inside', 0))
        self.symbol_outside = _SchPinSymbol(self.rawdata.get('symbol_outside', 0))   
        self.symbol_linewidth = _SchLineWidth(self.rawdata.get('symbol_linewidth', 0))
        
        self.description = self.rawdata.get('description', 0)
        self.name = self.rawdata.get('name', 0) 
        self.designator = self.rawdata.get('designator', 0)
        
        self.electrical_type = _SchPinElectricalType(self.rawdata.get('electrical_type', 0))  
        
        self.rotated = self.rawdata.get('rotated', 0)
        self.flipped = self.rawdata.get('flipped', 0)
        self.hide = self.rawdata.get('hide', 0)
        self.show_name = self.rawdata.get('show_name', 0)
        self.show_designator = self.rawdata.get('show_designator', 0) 
        
        self.graphically_locked = self.rawdata.get('graphically_locked', 0) 
        
        self.pinlength = self.rawdata.get('length', 0)
        
        
    def __repr__(self):
        return f"SchPin"
        

        
    



