"""
Schematic Data Types for Records
"""
from pyaltiumlib.datatypes import SchCoord, SchCoordPoint


class _SchCommonParam:
    
    def __init__(self, data):
        
        self.rawdata = {key.lower(): value for key, value in data.items()}

        self.record = int(self.rawdata.get('record', 0))
        self.is_not_accessible = self.rawdata.get('isnotaccessible', 'F').upper() == 'T'
        self.owner_index = int(self.rawdata.get('ownerindex', 0))
        self.owner_part_id = self.rawdata.get('ownerpartid', '0') == '1'
        self.owner_part_display_mode = int(self.rawdata.get('ownerpartdisplaymode', 0))
        self.graphically_locked = self.rawdata.get('graphicallylocked', 'F').upper() == 'T'
        self.unique_id = self.rawdata.get('uniqueid', '')


        self.location = SchCoordPoint(SchCoord.parse_dpx("location.x", self.rawdata),
                                       SchCoord.parse_dpx("location.y", self.rawdata, scale=-1.0))
        
        
        self.color = _SchColor(self.rawdata.get('color', 0))
        self.areacolor = _SchColor(self.rawdata.get('areacolor', 0))
        
        
# =============================================================================
#     Colors
# =============================================================================   
 
class _SchColor:
    
    def __init__(self, color):
        """
        Initializes the color from an integer representing the BGR value.
        :param color: The BGR color in 0xBBGGRR format.
        """
        
        self.color = int(color)
        
        self.blue = (self.color >> 16) & 0xFF
        self.green = (self.color >> 8) & 0xFF
        self.red = self.color & 0xFF 
        
    def __repr__(self):
        return f"{self.color}"          
        
    def to_hex(self):
        return f"#{self.red:02X}{self.green:02X}{self.blue:02X}"
