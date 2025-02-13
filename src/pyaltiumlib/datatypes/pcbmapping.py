from .mapping import MappingBase

class PCBPadShape(MappingBase):
    _map = {
        0: "None",
        1: "Round",
        2: "Rectangular",
        3: "Octagonal",
        9: "Rounded Rectangle"
    }
    
class PCBHoleShape(MappingBase):
    _map = {
        -1: "None",
        0: "Round",
        1: "Square",
        2: "Slot",
    }

class PCBStackMode(MappingBase):
    _map = {
        0: "Simple",
        1: "TopMiddleBottom",
        2: "FullStack",
    }

class PCBStrokeFont(MappingBase):
    _map = {
        0: "Default",
        1: "SansSerif",
        2: "Serif",
    }
    
class PCBTextKind(MappingBase):
    _map = {
        0: {"name": "Stroke", "default_font": "UHF"},
        1: {"name": "TrueType", "default_font": "Arial"},
        2: {"name": "BarCode", "default_font": "Arial"},
    } 
    
    def get_name(self):
        return self._map[self.value]["name"]
    
    def get_font(self):
        return self._map[self.value]["default_font"]

    def __eq__(self, other):
        if not isinstance(other, PCBTextKind):
            return False
        return (
            self.get_name() == other.get_name()
            and self.get_font() == other.get_font()
            )    

class PCBTextJustification(MappingBase):
    _map = {
        1: {"name": "BottomRight", "vertical": "text-after-edge", "horizontal": "start"},
        2: {"name": "MiddleRight", "vertical": "central", "horizontal": "start"},
        3: {"name": "TopRight", "vertical": "text-before-edge", "horizontal": "start"},
        4: {"name": "BottomCenter", "vertical": "text-after-edge", "horizontal": "middle"},
        5: {"name": "MiddleCenter", "vertical": "central", "horizontal": "middle"},
        6: {"name": "TopCenter", "vertical": "text-before-edge", "horizontal": "middle"},
        7: {"name": "BottomLeft", "vertical": "text-after-edge", "horizontal": "end"},
        8: {"name": "MiddleLeft", "vertical": "central", "horizontal": "end"},
        9: {"name": "TopLeft", "vertical": "text-before-edge", "horizontal": "end"},
    }
    
    def get_name(self):
        return self._map[self.value]["name"]

    def get_vertical(self):
        return self._map[self.value]["vertical"]
    
    def get_horizontal(self):
        return self._map[self.value]["horizontal"]