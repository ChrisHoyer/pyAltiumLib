from .mapping import MappingBase

class SchematicLineWidth(MappingBase):
    _map = {
        0: "Smallest",
        1: "Small",
        2: "Medium",
        3: "Large"
    }
    
    def __int__(self):
        if self.value == 0:
            return 1
        elif self.value == 1:
            return 1
        elif self.value == 2:
            return 3
        elif self.value == 3:
            return 5
        else:
            return 1
    

class SchematicLineStyle(MappingBase):
    _map = {
        0: "Solid",
        1: "Dashed",
        2: "Dotted",
        3: "Unknown"
    }
    


class SchematicLineShape(MappingBase):
    _map = {
        0: "None",
        1: "Arrow",
        2: "SolidArrow",
        3: "Tail",
        4: "SolidTail",
        5: "Circle",
        6: "Square"
    }
    
    def draw_marker(self, dwg, size_shape, color, end=False):
               
        marker = dwg.marker(insert=(0, 0), size=(10*size_shape, 10*size_shape), orient="auto", style="overflow:visible")
            
        arrow_x = size_shape * 0.75
        arrow_y = size_shape * 0.5
        arrow_tail = size_shape * 0.75
        circ_sqr = size_shape * 0.5
        
        if self.name == "Arrow":
            arrow_path = f"M{arrow_x},{arrow_y} 0,0 {arrow_x},{-arrow_y}"
            path = dwg.path(d=arrow_path, fill="none", stroke=color, 
                            stroke_linejoin="round", stroke_linecap="round")
            if end: path['transform'] = "rotate(180)"
            marker.add(path)

        if self.name == "Tail":
            arrow_path = f"M{-arrow_x},{-arrow_y} 0,0 {-arrow_x},{arrow_y}"
            path = dwg.path(d=arrow_path, fill="none", stroke=color, 
                            stroke_linejoin="round", stroke_linecap="round")
            if end: path['transform'] = "rotate(180)"
            marker.add(path)
            
            second_path = dwg.path(d=arrow_path, fill="none", stroke=color,
                                   stroke_linejoin="round", stroke_linecap="round", transform=f"translate({arrow_tail}, 0)")
            if end: second_path['transform'] = f"translate({-arrow_tail}, 0) rotate(180)"
            marker.add(second_path)

        if self.name == "SolidTail":
            arrow_path = f"M{-arrow_x},{-arrow_y} 0,0 {-arrow_x},{arrow_y} {-arrow_x+arrow_tail},{arrow_y} {arrow_tail},{0} {-arrow_x+arrow_tail},{-arrow_y} Z"
            path = dwg.path(d=arrow_path, fill=color, stroke=color,
                            stroke_linejoin="round", stroke_linecap="round")
            if end: path['transform'] = "rotate(180)"
            marker.add(path)
                        
        if self.name == "SolidArrow":
            arrow_path = f"M{arrow_x},{arrow_y} 0,0 {arrow_x},{-arrow_y} Z"
            path = dwg.path(d=arrow_path, fill=color, stroke=color, 
                            stroke_linejoin="round", stroke_linecap="round")
            if end: path['transform'] = "rotate(180)"
            marker.add(path)
            
        if self.name == "Circle":
            marker.add(dwg.circle((0, 0), r=circ_sqr, fill=color))
 
        if self.name == "Square":
            marker.add(dwg.rect((-circ_sqr, -circ_sqr), (2*circ_sqr, 2*circ_sqr), fill=color))
            
        # Add to definitions
        dwg.defs.add(marker)     
        
        return marker   
    
    
    
class SchematicPinSymbol(MappingBase):
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

class SchematicPinElectricalType(MappingBase):
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
    
class SchematicTextOrientation(MappingBase):
    _map = {
        0: "None",
        1: "Rotated 90 degrees",
        2: "Rotated 180 degrees",
        3: "Rotated 270 degrees",
    }

class SchematicTextJustification(MappingBase):
    _map = {
        0: {"name": "BottomLeft", "vertical": "text-after-edge", "horizontal": "start"},
        1: {"name": "BottomCenter", "vertical": "text-after-edge", "horizontal": "middle"},
        2: {"name": "BottomRight", "vertical": "text-after-edge", "horizontal": "end"},
        3: {"name": "MiddleLeft", "vertical": "central", "horizontal": "start"},
        4: {"name": "MiddleCenter", "vertical": "central", "horizontal": "middle"},
        5: {"name": "MiddleRight", "vertical": "central", "horizontal": "end"},
        6: {"name": "TopLeft", "vertical": "text-before-edge", "horizontal": "start"},
        7: {"name": "TopCenter", "vertical": "text-before-edge", "horizontal": "middle"},
        8: {"name": "TopRight", "vertical": "text-before-edge", "horizontal": "end"},
    }
    
    def get_name(self):
        return self._map[self.value]["name"]

    def get_vertical(self):
        return self._map[self.value]["vertical"]
    
    def get_horizontal(self):
        return self._map[self.value]["horizontal"]
    