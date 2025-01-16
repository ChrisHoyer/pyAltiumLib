"""
Schematic Data Types for Records
"""
from pyaltiumlib.datatypes import ParameterColor
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint

class _GenericSchRecord:
    
    def __init__(self, data, parent):
        
        self.Symbol = parent
        self.rawdata = data

        self.record = int(self.rawdata.get('record', 0))
        
        self.is_not_accessible = self.rawdata.get_bool('isnotaccessible')
        self.graphically_locked = self.rawdata.get_bool('graphicallylocked') 
       
        
        self.owner_index = int(self.rawdata.get('ownerindex', 0))
        self.owner_part_id = self.rawdata.get('ownerpartid', '0') == '1'
        self.owner_part_display_mode = int(self.rawdata.get('ownerpartdisplaymode', 0))
        self.unique_id = self.rawdata.get('uniqueid', '')


        self.location = CoordinatePoint(Coordinate.parse_dpx("location.x", self.rawdata),
                                       Coordinate.parse_dpx("location.y", self.rawdata, scale=-1.0))
        
        
        self.color = ParameterColor(self.rawdata.get('color', 0))
        self.areacolor = ParameterColor(self.rawdata.get('areacolor', 0))
        
        # Common Alignments
        self.spacing_label_name = 4.0
        self.spacing_label_designator = 1.0


    def draw_linestyle(self):
            
        if not hasattr(self, 'linestyle') and not hasattr(self, 'linestyle_ext'):
            raise AttributeError("Object must have either 'linestyle' or 'linestyle_ext' attribute")
        
        # dotted
        if self.linestyle.to_int() == 1 or self.linestyle_ext.to_int() == 1:
            return "4,10"
        
        # dashed
        if self.linestyle.to_int() == 2 or self.linestyle_ext.to_int() == 1:
            return "1,10"
        
        # dash-dotted
        if self.linestyle.to_int() == 3 or self.linestyle_ext.to_int() == 3:
            return "1,10,4,10"   
         
        # solid
        else:
            return "none"


    def draw_bounding_box(self, graphic, offset, zoom):
        """
        Draws a bounding box using svgwrite.
        """
        bbox = self.get_bounding_box()
        
        start = (bbox[0] * zoom) + offset
        end = (bbox[1] * zoom) + offset
        
        size = start - end
        start.y = start.y - size.y
        
        if size.y == 0:
            raise ValueError(f"RecordID: {self.record} - Invalid bounding box dimensions y: {bbox}")
        
        if size.x == 0:
            raise ValueError(f"RecordID: {self.record} - Invalid bounding box dimensions x: {bbox}")           
        
        graphic.add(
            graphic.rect(
                insert= start.get_int(),
                size=[ abs(x) for x in size.get_int() ],
                fill="none",
                stroke="black",
                stroke_width=1
            )
        )     