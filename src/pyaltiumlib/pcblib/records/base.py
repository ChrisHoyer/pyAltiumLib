import math

# Set up logging
import logging
logger = logging.getLogger(__name__)

class _GenericPCBRecord:
    
    def __init__(self, parent):
        
        self.Footprint = parent
        self.is_initialized = False
                
        
    def read_common(self, byte_array):
        
        if len(byte_array) != 13:
            raise ValueError("Byte array length is not as expected")     
        
        self.layer = byte_array[0]
                
        self.unlocked = bool( byte_array[1] & 0x04 ) 
        self.tenting_top = bool( byte_array[1] & 0x20 ) 
        self.tenting_bottom = bool( byte_array[1] & 0x40 ) 
        self.fabrication_top = bool( byte_array[1] & 0x80 ) 
        self.fabrication_bottom = bool( byte_array[2] & 0x01 ) 
        self.keepout = bool( byte_array[2] & 0x02 )
        
        if not all(byte == 0xFF for byte in byte_array[3:13]):
            raise ValueError("Byte array spacer is not as expected")

        
    def get_layer_by_id(self, layerid): 
        
        for layer in self.Footprint.LibFile.Layers:
            if layer.id == layerid: 
                return layer
            
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

    def draw_bounding_box(self, graphic, offset, zoom):
        """
        Draws a bounding box using svgwrite.
        """
        bbox = self.get_bounding_box()
        
        start = (bbox[0] * zoom) + offset
        end = (bbox[1] * zoom) + offset
        
        size = start - end
        #start.y = start.y - size.y
        
        if size.y == 0:
            raise ValueError(f"RecordID: {self.record} - Invalid bounding box dimensions y: {bbox}")
        
        if size.x == 0:
            raise ValueError(f"RecordID: {self.record} - Invalid bounding box dimensions x: {bbox}")           
        
        graphic.add(
            graphic.rect(
                insert= start.to_int_tuple(),
                size= abs(size).to_int_tuple(),
                fill="none",
                stroke="white",
                stroke_width=1
            )
        )   