from pyaltiumlib.pcblib.records.base import GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader, Coordinate, CoordinatePoint
from pyaltiumlib.datatypes import PCBPadShape, PCBHoleShape

from typing import Tuple

# Configure logging
import logging
logger = logging.getLogger(__name__)

class PcbPad(GenericPCBRecord):
    """
    Implementation of a pcb record
    See also :ref:`PCBPrimitive02` details on this PCB records. This record can be drawn.
    
    :param class parent: Parent symbol object 
    :param Dict data: Dictionary containing raw record data
    """
    
    def __init__(self, parent, stream):
        
        super().__init__(parent)        
        
        try:
            self.designator = BinaryReader.from_stream( stream ).read_string_block()
            
            # Unknown
            BinaryReader.from_stream( stream )
            BinaryReader.from_stream( stream ).read_string_block()
            BinaryReader.from_stream( stream )  
            
    
            first_block = BinaryReader.from_stream( stream )
            second_block = BinaryReader.from_stream( stream )
    
            # Read First Block 
            if first_block.has_content():
                self.read_common( first_block.read(13) )
                self.location = first_block.read_bin_coord()
                
                self.size_top = first_block.read_bin_coord()
                self.size_middle = first_block.read_bin_coord()
                self.size_bottom = first_block.read_bin_coord()
                self.hole_size = Coordinate.parse_bin(first_block.read(4))
                
                self.shape_top = PCBPadShape( first_block.read_int8() )
                self.shape_middle = PCBPadShape( first_block.read_int8() )
                self.shape_bottom = PCBPadShape( first_block.read_int8() )
                
                self.rotation = first_block.read_double() 
                self.is_plated = bool( first_block.read_int8() )
                
                first_block.read_byte() # Unknown
                
                self.stack_mode = first_block.read_int8()
                
                first_block.read_byte() # Unknown
                first_block.read_int32() # Unknown            
                first_block.read_int32() # Unknown    
                first_block.read_int16() # Unknown               
                first_block.read_int32() # Unknown    
                first_block.read_int32() # Unknown    
                first_block.read_int32() # Unknown    
                            
                self.expansion_paste_mask = Coordinate.parse_bin(first_block.read(4))
                self.expansion_solder_mask = Coordinate.parse_bin(first_block.read(4))
        
                first_block.read_byte() # Unknown
                first_block.read_byte() # Unknown
                first_block.read_byte() # Unknown
                first_block.read_byte() # Unknown
                first_block.read_byte() # Unknown
                first_block.read_byte() # Unknown
                first_block.read_byte() # Unknown
        
                self.expansion_manual_paste_mask = first_block.read_int8()
                self.expansion_manual_solder_mask = first_block.read_int8()
        
                first_block.read( 7 ) # Unknown 
                
                self.jumperid = first_block.read_int16()
            
                
            # Read Second Block
            if second_block.has_content():
                
                pad_x_size = [ Coordinate.parse_bin(second_block.read(4)) for x in range(29) ]
                pad_y_size = [ Coordinate.parse_bin(second_block.read(4)) for x in range(29) ]           
                self.size_middle_layers = [ CoordinatePoint(pad_x_size[i], pad_y_size[i]) for i in range(29)]
                
                self.shape_middle_layers = [ PCBPadShape( second_block.read_int8() ) for i in range(29)]
    
                second_block.read_byte() # Unknown
                
                self.hole_shape = PCBHoleShape( second_block.read_int8() )
                self.hole_slot_length = Coordinate.parse_bin(second_block.read(4))
                self.hole_rotation = second_block.read_double()
                
                hole_x_offset = [ Coordinate.parse_bin(second_block.read(4)) for x in range(32) ]
                hole_y_offset = [ Coordinate.parse_bin(second_block.read(4)) for x in range(32) ]           
                self.hole_offset = [ CoordinatePoint(hole_x_offset[i], hole_y_offset[i]) for i in range(32)]
                
                self.has_round_rect = bool( second_block.read_int8() )
                self.shape_layers = [ PCBPadShape( second_block.read_int8() ) for i in range(32)]
                self.corner_radius_percentage = [ second_block.read_int8() for i in range(32)]
                
            else:
                self.size_middle_layers = None
                self.shape_middle_layers = None
                self.hole_shape = PCBHoleShape(-1)
                self.hole_slot_length = None
                self.hole_rotation = None
                self.hole_offset = None
                self.has_round_rect = None
                self.shape_layers = None
                self.corner_radius_percentage = None
            
            if self.layer > 0: self.is_drawable = True
        
        except Exception as e:
            logger.error(f"Failed to parse PCB record: {str(e)}")
            
            
# =============================================================================
#     Drawing related
# ============================================================================= 

    def get_bounding_box(self) -> Tuple[CoordinatePoint, CoordinatePoint]:
        """
        Generates and returns a bounding box for this record
        
        :return: List with two coordinate entries 
        :rtype: tuple with :ref:`DataTypeCoordinatePoint`
        """
        
        size_x = max(float(abs(self.size_top.x)), float(abs(self.size_middle.x)), float(abs(self.size_bottom.x)))
        size_y = max(float(abs(self.size_top.y)), float(abs(self.size_middle.y)), float(abs(self.size_bottom.y)))
        
        size_x = size_x + self.expansion_solder_mask  if self.expansion_manual_solder_mask == 2 else size_x + 8
        size_y = size_y + self.expansion_solder_mask  if self.expansion_manual_solder_mask == 2 else size_y + 8
        
        corners = [
            CoordinatePoint(self.location.x - size_x / 2, self.location.y - size_y / 2),
            CoordinatePoint(self.location.x + size_x / 2, self.location.y - size_y / 2),
            CoordinatePoint(self.location.x + size_x / 2, self.location.y + size_y / 2),
            CoordinatePoint(self.location.x - size_x / 2, self.location.y + size_y / 2),
        ]
        
        rotated_corners = [corner.rotate(self.location, self.rotation) for corner in corners]

        xs = [corner.x for corner in rotated_corners]
        ys = [corner.y for corner in rotated_corners]

        min_x, min_y = min(xs), min(ys)
        max_x, max_y = max(xs), max(ys)
        
        return [CoordinatePoint(Coordinate(min_x), Coordinate(min_y)),
                CoordinatePoint(Coordinate(max_x), Coordinate(max_y))]

    
    def draw_svg(self, dwg, offset, zoom) -> None:
        """
        Draw pcb record using svgwrite.
        
        :param graphic dwg: svg drawing object
        :param CoordinatePoint offset: Move drawing by the given offset as :ref:`DataTypeCoordinatePoint`
        :param float zoom: Scaling Factor for all elements  
        """
        # Masks
        # TODO: for other shapes, there seems to be something incorrect.... Sanity check for solder mask necessary?
        # TODO: What happens if expansion_manual_solder_mask is not 2 or 0?
        solder_mask = self.expansion_solder_mask  if self.expansion_manual_solder_mask == 2 else Coordinate(8) 
                
        # Draw Pads
        # TODO: For now only Bottom and/or Top are implemented
        if self.layer == 1:
            if not self.tenting_top:
                self._draw_svg_pad_element(dwg, offset, zoom, self.size_top.expand(solder_mask), self.shape_top, 37, 1)
            self._draw_svg_pad_element(dwg, offset, zoom, self.size_top, self.shape_top, 1)
            
        elif self.layer == 32:
            if not self.tenting_bottom:
                self._draw_svg_pad_element(dwg, offset, zoom, self.size_bottom.expand(solder_mask), self.shape_bottom, 38, 32)
            self._draw_svg_pad_element(dwg, offset, zoom, self.size_bottom, self.shape_bottom, 32)
            
        elif self.layer == 74:
            if not self.tenting_top:
                self._draw_svg_pad_element(dwg, offset, zoom, self.size_top.expand(solder_mask), self.shape_top, 37, 1)
            self._draw_svg_pad_element(dwg, offset, zoom, self.size_top, self.shape_top, 1)   

            if not self.tenting_bottom:
                self._draw_svg_pad_element(dwg, offset, zoom, self.size_bottom.expand(solder_mask), self.shape_bottom, 38, 32)            
            self._draw_svg_pad_element(dwg, offset, zoom, self.size_bottom, self.shape_bottom, 32)
            
        
        # Draw hole
        if self.hole_size > 0:
            self._draw_svg_hole(dwg, offset, zoom, 81)
            

        center = (self.location.copy() * zoom) + offset 
        drawing_primitive = dwg.text(self.designator,
                                     insert = center.to_int_tuple(),
                                     fill = "white",
                                     dominant_baseline="central", text_anchor="middle",
                                     transform=f"rotate(-{self.rotation % 180} {center.x} {center.y})"
                                     )
        
        self.Footprint._graphic_layers[0].add( drawing_primitive )

                
# =============================================================================
#     Pad and Via Drawing related
# =============================================================================

    def _draw_svg_hole(self, dwg, offset, zoom, layer_id):
        """
        Subfunction to draw holes in different shapes
        """   
        
        hole_size_x = self.hole_size
        hole_size_y = self.hole_size
        
        # Square
        if self.hole_shape.to_int() == 1:
            hole_size_x = self.hole_slot_length
            corner_radius = 0
            
        # Slot
        elif self.hole_shape.to_int() == 2:
            hole_size_x = self.hole_slot_length
            corner_radius = 100
            
        # Round
        else:
            corner_radius = 100
        
        center = (self.location.copy() * zoom) + offset
        size = CoordinatePoint(hole_size_x, hole_size_y) * zoom
        start = center - size/2
        
        layer = self.get_layer_by_id(layer_id)
        
        path = self.get_svg_rounded_rect_path(start, size, layer_id, corner_radius)
        drawing_primitive = dwg.path(d=path,
                                     fill=layer.color.to_hex(),
                                     transform=f"rotate(-{self.rotation} {center.x} {center.y})")
        
        self.Footprint._graphic_layers[layer_id].add( drawing_primitive )
                      
        
    def _draw_svg_pad_element(self, dwg, offset, zoom, size, shape, plot_layer, ref_layer=None):
        """
        Subfunction to draw pads
        """       
        ref_layer = plot_layer if ref_layer == None else ref_layer
        
        center = (self.location.copy() * zoom) + offset
        start = ((self.location.copy() - (size / 2)) * zoom) + offset
        end = ((self.location.copy() + (size / 2)) * zoom) + offset
        
        size = abs( (start - end ).to_int() )
        start.y = start.y - size.y
        
        # Get the layer color
        layer = self.get_layer_by_id(plot_layer)
        
        if shape.to_int() == 1: 
                            
            path = self.get_svg_rounded_rect_path(start, size, plot_layer,
                                              self.corner_radius_percentage[ref_layer-1] if self.corner_radius_percentage else 100 )
            drawing_primitive = dwg.path(d=path,
                                         fill=layer.color.to_hex(),
                                         transform=f"rotate(-{self.rotation} {center.x} {center.y})"
                                         )
        
        elif shape.to_int() == 2:
            drawing_primitive = dwg.rect(insert = start.to_int_tuple(),
                                         size = abs(size).to_int_tuple(),
                                         fill = layer.color.to_hex(),
                                         transform=f"rotate(-{self.rotation} {center.x} {center.y})"
                                         )
    
        elif shape.to_int() == 3:
            
            edge_length =  min(size.y, size.x) / 2
            diagonal_offset = int(edge_length / 2)
            
            vertices = [
                (int(center.x - diagonal_offset), int(center.y - edge_length)),
                (int(center.x + diagonal_offset), int(center.y - edge_length)),
                (int(center.x + edge_length), int(center.y - diagonal_offset)),
                (int(center.x + edge_length), int(center.y + diagonal_offset)),
                (int(center.x + diagonal_offset), int(center.y + edge_length)),
                (int(center.x - diagonal_offset), int(center.y + edge_length)),
                (int(center.x - edge_length), int(center.y + diagonal_offset)),
                (int(center.x - edge_length), int(center.y - diagonal_offset)),
            ]
                
            drawing_primitive = dwg.polygon(points = vertices,
                                            fill = layer.color.to_hex(),
                                            transform=f"rotate(-{self.rotation} {center.x} {center.y})"
                                            )
          
            
        else:
            print(f"Unknown pad shape: {shape}")
            
        self.Footprint._graphic_layers[plot_layer].add( drawing_primitive )

        

       