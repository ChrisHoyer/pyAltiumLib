from pyaltiumlib.pcblib.records.base import GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader, CoordinatePoint, Coordinate, ParameterCollection
from typing import Tuple

# Configure logging
import logging
logger = logging.getLogger(__name__)

class PcbRegion(GenericPCBRecord):
    """
    Implementation of a pcb record
    See also :ref:`PCBPrimitive11` details on this PCB records. This record can be drawn.
    
    :param class parent: Parent symbol object 
    :param Dict data: Dictionary containing raw record data
    """
    def __init__(self, parent, stream):
        super().__init__(parent)

        try:
            block = BinaryReader.from_stream(stream)
            
            if block.has_content():

                self.read_common(block.read(13))

                block.read_int32() # Unknown                   
                block.read_byte() # Unknown

                self.parameter = ParameterCollection( block.read_string_block(size_string = 4))
                
                self.num_vertices = block.read_int32()                
                self.vertices = [ block.read_bin_coord( double=True ) for i in range(self.num_vertices)] 
                    
                    
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
                
            min_x = float("inf")
            min_y = float("inf")
            max_x = float("-inf")
            max_y = float("-inf")
        
            for vertex in self.vertices:
                min_x = min(min_x, float(vertex.x))
                min_y = min(min_y, float(vertex.y))
                max_x = max(max_x, float(vertex.x))
                max_y = max(max_y, float(vertex.y))
    
            return [CoordinatePoint(Coordinate(min_x), Coordinate(min_y)),
                    CoordinatePoint(Coordinate(max_x), Coordinate(max_y))]
                        
        except Exception as e:
            logger.error(f"Error calculating bounding box: {str(e)}")


    def draw_svg(self, dwg, offset, zoom) -> None:
        """
        Draw pcb record using svgwrite.
        
        :param graphic dwg: svg drawing object
        :param CoordinatePoint offset: Move drawing by the given offset as :ref:`DataTypeCoordinatePoint`
        :param float zoom: Scaling Factor for all elements  
        """
        if not self.vertices:
            logger.warning("No vertices found for polygon, skipping draw")
            return

        try:
            # Calculate scaled and offset coordinates   
            points = [(vertex * zoom + offset).to_int_tuple() for vertex in self.vertices]
            points.append(points[0])
            
            layer = self.get_layer_by_id(self.layer)
            
            region_fill = layer.color.to_hex()
            region_stroke = "none"
            region_stroke_dash = "none"
            region_stroke_width = 1
            
            if self.keepout:
                region_fill = self.get_svg_keepout_pattern( dwg, self.layer )
                region_stroke = layer.color.to_hex()
            
            elif self.parameter.get_bool("isboardcutout") or self.parameter.get_int("kind") > 0:
                region_fill = "none"
                region_stroke_width = 3
                region_stroke = layer.color.to_hex()
                region_stroke_dash = "10,10"
            
            drawing_primitive = dwg.polyline(points=points,
                                             fill=region_fill,
                                             stroke=region_stroke,
                                             stroke_width= region_stroke_width * zoom,
                                             stroke_dasharray=region_stroke_dash,
                                             stroke_linejoin="round",
                                             stroke_linecap="round"
                                             )
            
            self.Footprint._graphic_layers[self.layer].add(drawing_primitive)
            
        except Exception as e:
            logger.error(f"Failed to draw PCB Fill: {str(e)}")