from pyaltiumlib.schlib.records.base import GenericSchRecord
from pyaltiumlib.datatypes import SchematicLineWidth, SchematicPinSymbol, SchematicPinElectricalType, CoordinatePoint

from typing import Tuple

# Set up logging
import logging
logger = logging.getLogger(__name__)

class SchPin(GenericSchRecord):
    """
    Implementation of a schematic record
    See also :ref:`SchPrimitive02` details on this schematic records. This record can be drawn.
    
    :param Dict data: Dictionary containing raw record data
    :param class parent: Parent symbol object   
    :raises ValueError: If record id is not valid
    """
    
    def __init__(self, data, parent):
        
        super().__init__(data, parent)
        
        if not( self.record == 2 ):
            logger.warning(f"Error in mapping between record objects and record id! - incorrect id {self.record}")
        
        self.symbol_inneredge = SchematicPinSymbol(self.rawdata.get('symbol_inneredge', 0))
        self.symbol_outeredge = SchematicPinSymbol(self.rawdata.get('symbol_outeredge', 0))
        self.symbol_inside = SchematicPinSymbol(self.rawdata.get('symbol_inside', 0))
        self.symbol_outside = SchematicPinSymbol(self.rawdata.get('symbol_outside', 0))   
        self.symbol_linewidth = SchematicLineWidth(self.rawdata.get('symbol_linewidth', 0))
        
        self.description = self.rawdata.get('description', 0)
        self.name = self.rawdata.get('name', 0) 
        self.designator = self.rawdata.get('designator', 0)
        
        self.electrical_type = SchematicPinElectricalType(self.rawdata.get('electrical_type', 0))  
        
        self.rotated = self.rawdata.get('rotated', 0)
        self.flipped = self.rawdata.get('flipped', 0)
        self.hide = self.rawdata.get('hide', 0)
        self.show_name = bool( self.rawdata.get('show_name', 0) )
        self.show_designator = bool( self.rawdata.get('show_designator', 0) )
        
        self.graphically_locked = self.rawdata.get('graphically_locked', 0) 
        
        self.pinlength = self.rawdata.get('length', 0)
        
        self.is_drawable = True
          
    def get_bounding_box(self) -> Tuple[CoordinatePoint, CoordinatePoint]:
        """
        Generates and returns a bounding box for this record
        
        :return: List with two coordinate entries 
        :rtype: tuple with :ref:`DataTypeCoordinatePoint`
        """
        self.end = self.location.copy()
        self.label_name = {
            "vertical": "middle",
            "horizontal": "end",
            "rotation": 0,
            "position" : self.location.copy()
            }

        self.label_designator = {
            "vertical": "auto",
            "horizontal": "middle",
            "rotation": 0,
            "position" : self.location.copy()
            }
                
        if self.rotated and self.flipped:
            self.end.y = self.end.y + self.pinlength
            self.label_name["horizontal"] = "start" 
            self.label_name["rotation"] = -90 
            self.label_name["position"].y = self.label_name["position"].y - self.spacing_label_name
            self.label_designator["rotation"] = -90 
            self.label_designator["position"].y = self.label_designator["position"].y + 0.5 * self.pinlength
            self.label_designator["position"].x = self.label_designator["position"].x - self.spacing_label_designator
           
        if self.rotated and not self.flipped:
            self.end.y = self.end.y - self.pinlength
            self.label_name["horizontal"] = "end" 
            self.label_name["rotation"] = -90 
            self.label_name["position"].y = self.label_name["position"].y + self.spacing_label_name
            self.label_designator["rotation"] = -90 
            self.label_designator["position"].y = self.label_designator["position"].y - 0.5 * self.pinlength
            self.label_designator["position"].x = self.label_designator["position"].x - self.spacing_label_designator
                        
        if not self.rotated and self.flipped:
            self.end.x = self.end.x - self.pinlength
            self.label_name["horizontal"] = "start" 
            self.label_name["position"].x = self.label_name["position"].x + self.spacing_label_name
            self.label_designator["position"].x = self.label_designator["position"].x - 0.5 * self.pinlength
            self.label_designator["position"].y = self.label_designator["position"].y - self.spacing_label_designator
            
        if not self.rotated and not self.flipped:
            self.end.x = self.end.x + self.pinlength
            self.label_name["horizontal"] = "end"
            self.label_name["position"].x = self.label_name["position"].x - self.spacing_label_name
            self.label_designator["position"].x = self.label_designator["position"].x + 0.5 * self.pinlength
            self.label_designator["position"].y = self.label_designator["position"].y - self.spacing_label_designator
          
        return [self.location, self.end]
    
    def draw_svg(self, dwg, offset, zoom) -> None:
        """
        Draw schematic record using svgwrite.
        
        :param graphic dwg: svg drawing object
        :param CoordinatePoint offset: Move drawing by the given offset as :ref:`DataTypeCoordinatePoint`
        :param float zoom: Scaling Factor for all elements  
        """
        
        start = (self.location * zoom) + offset
        stop = (self.end * zoom) + offset
        position_name = (self.label_name["position"] * zoom) + offset
        position_designator = (self.label_designator["position"] * zoom) + offset
        
        if self.show_name:
            dwg.add(dwg.text(self.name,
                             font_size = self.Symbol.LibFile._Fonts[self.Symbol.LibFile._SystemFontID].size * zoom,
                             font_family = self.Symbol.LibFile._Fonts[self.Symbol.LibFile._SystemFontID].font,
                             insert = position_name.to_int_tuple(),
                             fill = self.color.to_hex(),
                             dominant_baseline = self.label_name["vertical"], 
                             text_anchor = self.label_name["horizontal"],
                             transform=f"rotate({self.label_name['rotation']} {int(position_name.x)} {int(position_name.y)})"
                             ))

        if self.show_designator:
            dwg.add(dwg.text(self.designator,
                             font_size = self.Symbol.LibFile._Fonts[self.Symbol.LibFile._SystemFontID].size * zoom,
                             font_family = self.Symbol.LibFile._Fonts[self.Symbol.LibFile._SystemFontID].font,
                             insert = position_designator.to_int_tuple(),
                             fill = self.color.to_hex(),
                             dominant_baseline = self.label_designator["vertical"], 
                             text_anchor = self.label_designator["horizontal"],
                             transform=f"rotate({self.label_designator['rotation']} {int(position_designator.x)} {int(position_designator.y)})"
                             ))
            
        dwg.add(dwg.line(start = start.to_int_tuple(),
                         end = stop.to_int_tuple(),
                         stroke= self.color.to_hex(),
                         stroke_width= 1 * zoom,
                         stroke_linecap="round"
                         ))
        
        

        
        
        
    



