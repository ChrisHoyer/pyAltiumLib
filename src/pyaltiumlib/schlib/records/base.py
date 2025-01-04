"""
Schematic Data Types for Records
"""

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


        self.location = _SchCoordPoint(_SchCoord("location.x", self.rawdata),
                                       _SchCoord("location.y", self.rawdata))
        
        
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


# =============================================================================
#     Coordinates
# =============================================================================   
 

class _SchCoord:
    
    def __init__(self, key, data):
        
        num = int(data.get(key, 0))
        frac = int(data.get(key + "_frac", 0))
        
        self.value =  num + frac / 1000.0;
        
    def __repr__(self):
        return f"{self.value}"       


class _SchCoordPoint:
    
    def __init__(self, x, y):
        if not isinstance(x, _SchCoord) or not isinstance(y, _SchCoord):
            raise TypeError("x and y must be instances of Coordinate")
            
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x};{self.y})"    
    
# =============================================================================
#     Mapping Datatypes
# =============================================================================   

class _SchMappingBase:
    
    def __init__(self, value: int):
        if int(value) not in self._map:
            raise ValueError(f"Invalid value: {value}")
        self.value = int(value)
        self.name = self._map[int(value)]

    def __repr__(self):
        return f"{self.name}"

    def to_int(self):
        return self.value


class _SchLineWidth(_SchMappingBase):
    _map = {
        0: "Smallest",
        1: "Small",
        2: "Medium",
        3: "Large"
    }

class _SchLineStyle(_SchMappingBase):
    _map = {
        0: "Solid",
        1: "Dashed",
        2: "Dotted"
    }

class _SchLineShape(_SchMappingBase):
    _map = {
        0: "None",
        1: "Arrow",
        2: "SolidArrow",
        3: "Tail",
        4: "SolidTail",
        5: "Circle",
        6: "Square"
    }
    
class _SchPinSymbol(_SchMappingBase):
    _map = {
        0: "NoneType",
        1: "Dot",
        2: "RightLeftSignalFlow",
        3: "Clock",
        4: "ActiveLowInput",
        5: "AnalogSignalIn",
        6: "NotLogicConnection",
        8: "PostponedOutput",
        9: "OpenCollector",
        10: "HiZ",
        11: "HighCurrent",
        12: "Pulse",
        13: "Schmitt",
        17: "ActiveLowOutput",
        22: "OpenCollectorPullUp",
        23: "OpenEmitter",
        24: "OpenEmitterPullUp",
        25: "DigitalSignalIn",
        30: "ShiftLeft",
        32: "OpenOutput",
        33: "LeftRightSignalFlow",
        34: "BidirectionalSignalFlow"
    }

class _SchPinElectricalType(_SchMappingBase):
    _map = {
        0: "Input",
        1: "InputOutput",
        2: "Output",
        3: "OpenCollector",
        4: "Passive",
        5: "HiZ",
        6: "OpenEmitter",
        7: "Power"
    }
    
class _SchTextOrientation(_SchMappingBase):
    _map = {
        0: "None",
        1: "Rotated",
        2: "Flipped",
    }

class _SchTextJustification(_SchMappingBase):
    _map = {
        0: "BottomLeft",
        1: "BottomCenter",
        2: "BottomRight",
        3: "MiddleLeft",
        4: "MiddleCenter",
        5: "MiddleRight",
        6: "TopLeft",
        7: "TopCenter",
        8: "TopRight"
    }