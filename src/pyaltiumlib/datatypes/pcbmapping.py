from .mapping import _MappingBase

class PCBPadShape(_MappingBase):
    _map = {
        0: "None",
        1: "Round",
        2: "Rectangular",
        3: "Octagonal",
        9: "Rounded Rectangle"
    }
    
class PCBHoleShape(_MappingBase):
    _map = {
        -1: "None",
        0: "Round",
        1: "Square",
        2: "Slot",
    }

class PCBStackMode(_MappingBase):
    _map = {
        0: "Simple",
        1: "TopMiddleBottom",
        2: "FullStack",
    }
    
class PCBTextJustification(_MappingBase):
    _map = {
        1: {"name": "BottomRight", "vertical": "text-after-edge", "horizontal": "end"},
        2: {"name": "MiddleRight", "vertical": "central", "horizontal": "end"},
        3: {"name": "TopRight", "vertical": "text-before-edge", "horizontal": "end"},
        4: {"name": "BottomCenter", "vertical": "text-after-edge", "horizontal": "middle"},
        5: {"name": "MiddleCenter", "vertical": "central", "horizontal": "middle"},
        6: {"name": "TopCenter", "vertical": "text-before-edge", "horizontal": "middle"},
        7: {"name": "BottomLeft", "vertical": "text-after-edge", "horizontal": "start"},
        8: {"name": "MiddleLeft", "vertical": "central", "horizontal": "start"},
        9: {"name": "TopLeft", "vertical": "text-before-edge", "horizontal": "start"},
    }
    
    def get_name(self):
        return self._map[self.value]["name"]

    def get_vertical(self):
        return self._map[self.value]["vertical"]
    
    def get_horizontal(self):
        return self._map[self.value]["horizontal"]