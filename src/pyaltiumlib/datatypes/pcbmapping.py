from .mapping import MappingBase

class PCBLayerKind(MappingBase):
    _map = {
        0x00: "Unspecified",
        0x01: "TopAssembly",
        0x02: "BottomAssembly",
        0x03: "AssemblyNotes",
        0x04: "BoardOutline",
        0x05: "TopConformalCoating",
        0x06: "BottomConformalCoating",
        0x07: "TopComponentCenter",
        0x08: "BottomComponentCenter",
        0x09: "TopComponentOutline",
        0x0A: "BottomComponentOutline",
        0x0B: "TopCourtyard",
        0x0C: "BottomCourtyard",
        0x0D: "TopDesignator",
        0x0E: "BottomDesignator",
        0x13: "TopGlue",
        0x14: "BottomGlue",
        0x17: "TopComponentValue",
        0x18: "BottomComponentValue",
        0x19: "VCutScoring",
        0x1A: "Top3DBody",
        0x1B: "Bottom3DBody",
        0x1C: "RoutingToolPaths",
    }

    # Values are in BGR (0xBBGGRR) — ParameterColor stores blue in the high byte.
    # Comments show the resulting screen colour as #RRGGBB.
    _colors = {
        0x01: 0xC09020,  # TopAssembly            — #2090C0 blue
        0x02: 0xC0C020,  # BottomAssembly         — #20C0C0 teal
        0x03: 0x80FFFF,  # AssemblyNotes          — #FFFF80 light yellow
        0x04: 0x00C0E0,  # BoardOutline           — #E0C000 yellow
        0x05: 0x80FF80,  # TopConformalCoating    — #80FF80 light green
        0x06: 0x008000,  # BottomConformalCoating — #008000 green
        0x07: 0xFF00FF,  # TopComponentCenter     — #FF00FF magenta
        0x08: 0xFF80FF,  # BottomComponentCenter  — #FF80FF lighter magenta
        0x09: 0xC0C000,  # TopComponentOutline    — #00C0C0 cyan
        0x0A: 0x808000,  # BottomComponentOutline — #008080 dark cyan
        0x0B: 0x00CCFF,  # TopCourtyard           — #FFCC00 amber
        0x0C: 0x60E0FF,  # BottomCourtyard        — #FFE060 lighter amber
        0x0D: 0xFFFFFF,  # TopDesignator          — #FFFFFF white
        0x0E: 0xC0C0C0,  # BottomDesignator       — #C0C0C0 light grey
        0x13: 0x0000C0,  # TopGlue                — #C00000 red
        0x14: 0x000080,  # BottomGlue             — #800000 dark red
        0x17: 0xFFFFFF,  # TopComponentValue      — #FFFFFF white
        0x18: 0xC0C0C0,  # BottomComponentValue   — #C0C0C0 light grey
        0x19: 0xFFFF00,  # VCutScoring            — #00FFFF cyan
        0x1A: 0x808080,  # Top3DBody              — #808080 grey
        0x1B: 0x404040,  # Bottom3DBody           — #404040 dark grey
        0x1C: 0x0080FF,  # RoutingToolPaths       — #FF8000 orange
    }

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