from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint
import math

# Set up logging
import logging
logger = logging.getLogger(__name__)

class GenericPCBRecord:
    """
    Base class for all PCB records in altium library. 
    See also :ref:`PCBPrimitveHeader` for more details on PCB records.
    
    :param class parent: Parent symbol object    
    """
    
    def __init__(self, parent):
        
        self.Footprint = parent
        self.is_drawable = False
                
    def __repr__(self) -> str:
        """
        :return: A string representation of the record object
        :rtype: str
        """
        return f"{self.__class__.__name__}"
        
    def read_common(self, byte_array):
        """
        Read PCB Record common parameters from byte array. The length of
        the byte array has to be 13 bytes.
        
        :param bytes byte_array: Array with common parameters for footprint records    
        """        
        if len(byte_array) != 13:
            logger.error("PCB reecord common parameters array length is not 13!")
        
        self.layer = byte_array[0]
                
        self.unlocked = bool( byte_array[1] & 0x04 ) 
        self.tenting_top = bool( byte_array[1] & 0x20 ) 
        self.tenting_bottom = bool( byte_array[1] & 0x40 ) 
        self.fabrication_top = bool( byte_array[1] & 0x80 ) 
        self.fabrication_bottom = bool( byte_array[2] & 0x01 ) 
        self.keepout = bool( byte_array[2] & 0x02 )
        
        if not all(byte == 0xFF for byte in byte_array[3:13]):
            logger.error("PCB record common parameters array spacer is not as expected")

        
    def get_layer_by_id(self, layerid): 
        """
        Retrieves the layer by the layer id given by the reocrd.

        :return: The record ID, or None if not found.
        :rtype: Layer or None
        """        
        for layer in self.Footprint.LibFile.Layers:
            if layer.id == layerid: 
                return layer
        
        logger.error(f"Can not find layer ID: {layerid}")
        return None

        
    def get_svg_arc_path(self, center, radius_x, radius_y, angle_start, angle_end):
        """
        This function returns the svg path data for an arc.
    
        :param tuple center: The center coordinates of the arc
        :param int radius_x: The x-radius of the arc
        :param int radius_y: The y-radius of the arc
        :param float angle_start: The start angle of the arc
        :param float angle_end: The end angle of the arc.
    
        :return: corresponding svg path data for arc
        """
        def degrees_to_radians(degrees):
            return (degrees * math.pi / 180) % (2*math.pi)
        
        angle_start = degrees_to_radians(angle_start)
        angle_stop = degrees_to_radians(angle_end)
        
        if angle_start == angle_stop:
            angle_stop -= 0.001
        
        start_x = center[0] + radius_x * math.cos(-angle_start)
        start_y = center[1] + radius_y * math.sin(-angle_start)
        end_x = center[0] + radius_x * math.cos(-angle_stop)
        end_y = center[1] + radius_y * math.sin(-angle_stop)
        
        # Set large_arc_flag based on the angle difference
        large_arc_flag = 1 if (angle_stop - angle_start) % (2 * math.pi) > math.pi else 0
        
        # Set sweep_flag to 0 for counterclockwise
        sweep_flag = 0
        
        path_data = (
            f"M {start_x},{start_y} "
            f"A {radius_x},{radius_y} 0 {large_arc_flag},{sweep_flag} {end_x},{end_y}"
        )
        return path_data


    def get_svg_rounded_rect_path(self, start, size, layer_id, radius_percentage = 100):
        """
        This function returns the svg path data for a rounded rectangle.
    
        :param CoordinatePoint start: The start coordinates of the rounded rectangle
        :param CoordinatePoint size: The size coordinates of the rounded rectangle
        :param int layer_id: The layer id of the rounded rectangle
        :param float radius_percentage: The start angle of the arc
    
        :return: corresponding svg path data for arc
        """        
        radius = (min(size.x, size.y) / 2) *  radius_percentage / 100 + 0.01
                 
        path_data = [
            f"M {int(start.x + radius)} {int(start.y)}",
            f"L {int(start.x + size.x - radius)} {int(start.y)}",
            f"A {abs(int(radius))} {abs(int(radius))} 0 0 1 {int(start.x + size.x)} {int(start.y + radius)}",
            f"L {int(start.x + size.x)} {int(start.y + size.y - radius)}",
            f"A {abs(int(radius))} {abs(int(radius))} 0 0 1 {int(start.x + size.x - radius)} {int(start.y + size.y)}",
            f"L {int(start.x + radius)} {int(start.y + size.y)}",
            f"A {abs(int(radius))} {abs(int(radius))} 0 0 1 {int(start.x)} {int(start.y + size.y - radius)}",
            f"L {int(start.x)} {int(start.y + radius)}",
            f"A {abs(int(radius))} {abs(int(radius))} 0 0 1 {int(start.x + radius)} {int(start.y)}",
            "Z"
        ]
        
        return " ".join(path_data)

    def get_svg_keepout_pattern(self, graphic, layer_id, size=10, stroke=1) -> None:
        """
        This function returns and defines the svg keep out pattern.
        
        :param graphic dwg: svg drawing object
        :param int layer_id: The layer id of the object
        :param int size: The size of the pattern
        :param int stroke: The stroke of the pattern
        
        Draws a bounding box using the values given by :code:`get_bounding_box`
        for each record
        """
        layer = self.get_layer_by_id(layer_id)
        
        keepout_pattern = graphic.defs.add(graphic.pattern(id="keepout_pattern", patternUnits="userSpaceOnUse", size=(size, size)))
        keepout_pattern.add(graphic.line(start=(0, 0), end=(size, size), stroke=layer.color.to_hex(), stroke_width=stroke))
        keepout_pattern.add(graphic.line(start=(0, size), end=(size, 0), stroke=layer.color.to_hex(), stroke_width=stroke))

        return "url(#keepout_pattern)"

    def draw_bounding_box(self, graphic, offset: CoordinatePoint, zoom: float) -> None:
        """
        This function is triggered when the :code:`draw_bbox` parameter is set in 
        :py:mod:`pyaltiumlib.libcomponent.LibComponent.draw_svg`.
        
        Draws a bounding box using the values given by :code:`get_bounding_box`
        for each record
        """
        try:
            bbox = self.get_bounding_box()
            if bbox is None:
                logger.warning("No bounding box available for record")
                return

            start = (bbox[0] * zoom) + offset
            end = (bbox[1] * zoom) + offset
            
            lower_left_x = min(start.x, end.x)
            lower_left_y = min(start.x, end.y)
            insert = CoordinatePoint( Coordinate(lower_left_x), Coordinate(lower_left_y) )
            
            size = start - end
            
            # Validate dimensions
            if size.y == 0 or size.x == 0:
                logger.error(f"Invalid bounding box dimensions: {size}")

            # Add rectangle to SVG
            graphic.add(
                graphic.rect(
                    insert=insert.to_int_tuple(),
                    size=[abs(x) for x in size.to_int_tuple()],
                    fill="none",
                    stroke="black",
                    stroke_width=1
                )
            )
        except Exception as e:
            logger.error(f"Failed to draw bounding box: {str(e)}")