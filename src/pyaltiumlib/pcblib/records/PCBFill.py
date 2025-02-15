from pyaltiumlib.pcblib.records.base import GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader, Coordinate, CoordinatePoint
from typing import Tuple

# Configure logging
import logging
logger = logging.getLogger(__name__)

class PcbFill(GenericPCBRecord):
    """
    Implementation of a pcb record
    See also :ref:`PCBPrimitive06` details on this PCB records. This record can be drawn.
    
    :param class parent: Parent symbol object 
    :param Dict data: Dictionary containing raw record data
    """
    def __init__(self, parent, stream):
        super().__init__(parent)

        try:
            block = BinaryReader.from_stream(stream)
            
            if block.has_content():

                self.read_common(block.read(13))
                self.corner1 = block.read_bin_coord()
                self.corner2 = block.read_bin_coord()
                self.rotation = block.read_double()
                
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
        try:
            
            self.center = (self.corner1 + self.corner2)/2
            
            corners = [self.corner1.copy(), self.corner2.copy()]
            return [corner.rotate(self.center, -self.rotation) for corner in corners]
                    
        except Exception as e:
            logger.error(f"Error calculating bounding box: {str(e)}")


    def draw_svg(self, dwg, offset, zoom) -> None:
        """
        Draw pcb record using svgwrite.
        
        :param graphic dwg: svg drawing object
        :param CoordinatePoint offset: Move drawing by the given offset as :ref:`DataTypeCoordinatePoint`
        :param float zoom: Scaling Factor for all elements  
        """
        try:
            # Calculate scaled and offset coordinates   
            start = (self.corner1 * zoom) + offset
            end = (self.corner2 * zoom) + offset
            center = (self.center * zoom) + offset
            
            # start is lower left corner -> needs to be upper right
            size = start - end
            start.y = start.y - size.y
            
            layer = self.get_layer_by_id(self.layer)

            region_fill = layer.color.to_hex()
            region_stroke = "none"
            
            if self.keepout:
                region_fill = self.get_svg_keepout_pattern( dwg, self.layer )
                region_stroke = layer.color.to_hex()
                
            drawing_primitive = dwg.rect(insert=start.to_int_tuple(),
                                         size=[abs(x) for x in size.to_int_tuple()],
                                         fill=region_fill,
                                         stroke=region_stroke,
                                         stroke_width=zoom,
                                         stroke_linejoin="round",
                                         stroke_linecap="round",
                                         transform=f"rotate(-{self.rotation} {center.x} {center.y})"
                                         )
            
            self.Footprint._graphic_layers[self.layer].add(drawing_primitive)
            
        except Exception as e:
            logger.error(f"Failed to draw PCB Fill: {str(e)}")