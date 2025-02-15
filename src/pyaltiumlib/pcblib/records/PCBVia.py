from pyaltiumlib.pcblib.records.base import GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader, Coordinate, CoordinatePoint
from pyaltiumlib.datatypes import PCBPadShape, PCBHoleShape

from typing import Tuple

# Configure logging
import logging
logger = logging.getLogger(__name__)

class PcbVia(GenericPCBRecord):
    """
    Implementation of a pcb record
    See also :ref:`PCBPrimitive03` details on this PCB records. This record can be drawn.
    
    :param class parent: Parent symbol object 
    :param Dict data: Dictionary containing raw record data
    """
    
    def __init__(self, parent, stream):
        
        super().__init__(parent)        
        
        try:
    
            block = BinaryReader.from_stream( stream )
    
            # Read Block 
            if block.has_content():
                
                self.read_common( block.read(13) )
                
                self.location = block.read_bin_coord()
                self.diameter = Coordinate.parse_bin(block.read(4))
                self.hole_size = Coordinate.parse_bin(block.read(4))
                self.layer_from = block.read_byte()
                self.layer_to = block.read_byte()
                
                block.read_byte() # Unknown
                
                self.thermalreleifairgapwidth = block.read_int32(signed = True)
                self.thermalreliefconductors = block.read_byte()
                
                block.read( 12 ) # Unknown
                
                self.expansion_solder_mask = Coordinate.parse_bin(block.read(4))
                
                block.read( 32 ) # Unknown
                
                self.expansion_manual_solder_mask = block.read_int8()
                
                block.read( 7 ) # Unknown
                
                self.diameter_stack_mode = block.read_int8()
                self.diameter_layer = [ ( block.read_int32( signed=True ) ) for i in range(32)]              

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
        
        size_x = self.diameter + self.expansion_solder_mask  if self.expansion_manual_solder_mask == 2 else self.diameter + 8
        size_y = self.diameter + self.expansion_solder_mask  if self.expansion_manual_solder_mask == 2 else self.diameter + 8
        
        return [ CoordinatePoint(self.location.x - size_x / 2, self.location.y - size_y / 2),
                 CoordinatePoint(self.location.x - size_x / 2, self.location.y + size_y / 2) ]

    
    def draw_svg(self, dwg, offset, zoom) -> None:
        """
        Draw pcb record using svgwrite.
        
        :param graphic dwg: svg drawing object
        :param CoordinatePoint offset: Move drawing by the given offset as :ref:`DataTypeCoordinatePoint`
        :param float zoom: Scaling Factor for all elements
        """
                        
        # Draw Pads
        if not self.tenting_top:
            self._draw_svg_pad_element(dwg, offset, zoom,  37, 1)
        self._draw_svg_pad_element(dwg, offset, zoom, 1)   

        if not self.tenting_bottom:
            self._draw_svg_pad_element(dwg, offset, zoom, 38, 32)            
        self._draw_svg_pad_element(dwg, offset, zoom, 32)
            
        # Draw hole
        if self.hole_size > 0:
            self._draw_svg_hole(dwg, offset, zoom, 81)

# =============================================================================
#     Pad and Via Drawing related
# =============================================================================

    def _draw_svg_hole(self, dwg, offset, zoom, layer_id):
        """
        Subfunction to draw holes
        """   
        
        center = (self.location.copy() * zoom) + offset
        size = CoordinatePoint(self.hole_size, self.hole_size) * zoom
        start = center - size/2
        
        layer = self.get_layer_by_id(layer_id)
        
        path = self.get_svg_rounded_rect_path(start, size, layer_id)
        drawing_primitive = dwg.path(d=path,
                                     fill=layer.color.to_hex())
        
        self.Footprint._graphic_layers[layer_id].add( drawing_primitive )
                      
        
    def _draw_svg_pad_element(self, dwg, offset, zoom, plot_layer, ref_layer=None):
        """
        Subfunction to draw pads
        """       
        ref_layer = plot_layer if ref_layer == None else ref_layer
        
        center = (self.location.copy() * zoom) + offset
        size = CoordinatePoint(self.diameter, self.diameter) * zoom
        start = center - size/2
        
        # Get the layer color
        layer = self.get_layer_by_id(plot_layer)
                 
        path = self.get_svg_rounded_rect_path(start, size, plot_layer, 100 )
        drawing_primitive = dwg.path(d=path,
                                     fill=layer.color.to_hex() )
            
        self.Footprint._graphic_layers[plot_layer].add( drawing_primitive )