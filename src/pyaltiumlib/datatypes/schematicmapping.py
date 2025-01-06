"""
Schematic Data Types for Records
"""
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


class SchematicLineWidth(_SchMappingBase):
    _map = {
        0: "Smallest",
        1: "Small",
        2: "Medium",
        3: "Large"
    }
    
    def __int__(self):
        if self.value == 0:
            return 2
        elif self.value == 1:
            return 4
        elif self.value == 2:
            return 6
        elif self.value == 3:
            return 10
        else:
            return 2
    

class SchematicLineStyle(_SchMappingBase):
    _map = {
        0: "Solid",
        1: "Dashed",
        2: "Dotted"
    }

class SchematicLineShape(_SchMappingBase):
    _map = {
        0: "None",
        1: "Arrow",
        2: "SolidArrow",
        3: "Tail",
        4: "SolidTail",
        5: "Circle",
        6: "Square"
    }
    
class SchematicPinSymbol(_SchMappingBase):
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

class SchematicPinElectricalType(_SchMappingBase):
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
    
class SchematicTextOrientation(_SchMappingBase):
    _map = {
        0: "None",
        1: "Rotated",
        2: "Flipped",
    }

class SchematicTextJustification(_SchMappingBase):
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