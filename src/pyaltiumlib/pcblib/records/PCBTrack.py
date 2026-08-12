from pyaltiumlib.pcblib.records.base import GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader, Coordinate, CoordinatePoint
from typing import Tuple

# Configure logging
import logging
logger = logging.getLogger(__name__)

class PcbTrack(GenericPCBRecord):
    """
    Implementation of a pcb record
    See also :ref:`PCBPrimitive04` details on this PCB records. This record can be drawn.
    
    :param class parent: Parent symbol object 
    :param Dict data: Dictionary containing raw record data
    """
    def __init__(self, parent, stream):
        super().__init__(parent)

        try:
            block = BinaryReader.from_stream(stream)
            
            if block.has_content():
                # Read common properties (e.g., layer, flags)
                self.read_common(block.read(13))
                
                # Read track-specific properties
                self.start = block.read_bin_coord()
                self.end = block.read_bin_coord()
                self.linewidth = Coordinate.parse_bin(block.read(4))
                self._apply_extended_layer(block.data[block.offset:])

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
            half_width = float(self.linewidth) / 2
            
            # Calculate min/max coordinates, including track width
            min_x = min(float(self.start.x), float(self.end.x)) - half_width
            min_y = min(float(self.start.y), float(self.end.y)) - half_width
            max_x = max(float(self.start.x), float(self.end.x)) + half_width
            max_y = max(float(self.start.y), float(self.end.y)) + half_width
            
            return (
                CoordinatePoint(Coordinate(min_x), Coordinate(min_y)),
                CoordinatePoint(Coordinate(max_x), Coordinate(max_y))
            )
        except Exception as e:
            logger.error(f"Error calculating bounding box: {str(e)}")
            return self.start, self.end


    def draw_svg(self, dwg, offset, zoom) -> None:
        """
        Draw pcb record using svgwrite.
        
        :param graphic dwg: svg drawing object
        :param CoordinatePoint offset: Move drawing by the given offset as :ref:`DataTypeCoordinatePoint`
        :param float zoom: Scaling Factor for all elements  
        """
        try:
            # Calculate scaled and offset coordinates
            start = (self.start * zoom) + offset
            end = (self.end * zoom) + offset
            
            # Get the layer color
            layer = self.get_layer_by_id(self.layer)
            if layer is None:
                logger.error(f"Invalid layer ID: {self.layer}")
            
            # Draw the track as an SVG line
            drawing_primitive = dwg.line(
                start=start.to_int_tuple(),
                end=end.to_int_tuple(),
                stroke=layer.color.to_hex(),
                stroke_width=int(self.linewidth) * zoom,
                stroke_linejoin="round",
                stroke_linecap="round"
            )
            
            self.Footprint._graphic_layers[self.layer].add(drawing_primitive)
            
        except Exception as e:
            logger.error(f"Failed to draw PCB track: {str(e)}")