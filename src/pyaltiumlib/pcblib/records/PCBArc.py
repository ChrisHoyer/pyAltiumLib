from pyaltiumlib.pcblib.records.base import GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader, Coordinate, CoordinatePoint

from typing import Tuple

# Configure logging
import logging
logger = logging.getLogger(__name__)

class PcbArc(GenericPCBRecord):
    """
    Implementation of a pcb record
    See also :ref:`PCBPrimitive01` details on this PCB records. This record can be drawn.
    
    :param class parent: Parent symbol object 
    :param Dict data: Dictionary containing raw record data
    """

    def __init__(self, parent, stream):
        super().__init__(parent)

        try:
            block = BinaryReader.from_stream(stream)
            
            if block.has_content():
                
                if block.length() > 67:
                # TODO: ERROR. To long!
                    return
                
                self.read_common(block.read(13))
                self.location = block.read_bin_coord()
                self.radius =  Coordinate.parse_bin(block.read(4))
                self.angle_start = block.read_double() 
                self.angle_end = block.read_double() 
                self.linewidth = Coordinate.parse_bin(block.read(4))
                
            if self.layer > 0: self.is_drawable = True
                
        except Exception as e:
            logger.error(f"Failed to parse PCB record: {str(e)}")
            raise

# =============================================================================
#     Drawing related
# ============================================================================= 


    def get_bounding_box(self) -> Tuple[CoordinatePoint, CoordinatePoint]:
        """
        Generates and returns a bounding box for this record
        
        :return: List with two coordinate entries 
        :rtype: tuple with :ref:`DataTypeCoordinatePoint`
        """
        start_x = self.location.x - self.radius
        start_y = self.location.y - self.radius
        end_x = self.location.x + self.radius
        end_y = self.location.y + self.radius

        min_x = min(self.location.x, start_x, end_x)
        max_x = max(self.location.x, start_x, end_x)
        min_y = min(self.location.y, start_y, end_y)
        max_y = max(self.location.y, start_y, end_y)
        
        return [CoordinatePoint(min_x, min_y), CoordinatePoint(max_x, max_y)]

    def draw_svg(self, dwg, offset, zoom) -> None:
        """
        Draw pcb record using svgwrite.
        
        :param graphic dwg: svg drawing object
        :param CoordinatePoint offset: Move drawing by the given offset as :ref:`DataTypeCoordinatePoint`
        :param float zoom: Scaling Factor for all elements  
        """
        center = (self.location * zoom) + offset
        radius = self.radius * zoom
        
        # Get the layer color
        layer = self.get_layer_by_id(self.layer)
        if layer is None:
            raise ValueError(f"Invalid layer ID: {self.layer}")

        arc_path = self.get_svg_arc_path(center.to_int_tuple(),
                                         int(radius), int(radius),
                                         self.angle_start, self.angle_end)

        drawing_primitive = dwg.path(d=arc_path,
                                     fill="none",
                                     stroke=layer.color.to_hex(),
                                     stroke_width=int(self.linewidth) * zoom,
                                     stroke_linejoin="round",
                                     stroke_linecap="round")
                
        # Add the line to the appropriate drawing layer
        self.Footprint._graphic_layers[self.layer].add(drawing_primitive)


