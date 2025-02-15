from pyaltiumlib.datatypes import ParameterColor
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint

from typing import Dict, Any
import math

# Configure logging
import logging
logger = logging.getLogger(__name__)

class GenericSchRecord:
    """
    Base class for all schematic records in altium library. 
    See also :ref:`SchRecord` and :ref:`SchCommonParameter` for more
    details on schematic records.
    
    :param Dict data: Dictionary containing raw record data
    :param class parent: Parent symbol object    
    """

    def __init__(self, data: Dict[str, Any], parent: [Any] = None):
        self.Symbol = parent
        self.rawdata = data
        self.is_drawable = False

        # Parse record metadata
        self.record = int(self.rawdata.get('record', 0))
        self.is_not_accessible = self.rawdata.get_bool('isnotaccessible', False)
        self.graphically_locked = self.rawdata.get_bool('graphicallylocked', False)
        
        # Parse ownership information
        self.owner_index = int(self.rawdata.get('ownerindex', 0))
        self.owner_part_id = self.rawdata.get('ownerpartid', '0') == '1'
        self.owner_part_display_mode = int(self.rawdata.get('ownerpartdisplaymode', 0))
        self.unique_id = self.rawdata.get('uniqueid', '')

        # Parse location and colors
        self.location = CoordinatePoint(
            Coordinate.parse_dpx("location.x", self.rawdata),
            Coordinate.parse_dpx("location.y", self.rawdata, scale=-1.0)
        )
        self.color = ParameterColor(self.rawdata.get('color', 0))
        self.areacolor = ParameterColor(self.rawdata.get('areacolor', 0))

        # Default spacing values
        self.spacing_label_name = 4.0
        self.spacing_label_designator = 1.0

    def __repr__(self) -> str:
        """
        :return: A string representation of the record object
        :rtype: str
        """
        return f"{self.__class__.__name__}"

    def get_svg_stroke_dasharray(self) -> str:
        """
        This function returns the svg attribute :code:`stroke-dasharray` for the given
        linestyle.
        
        For more information on how `stroke-dasharray` works, visit the 
        `MDN Web Docs for stroke-dasharray <https://developer.mozilla.org/de/docs/Web/SVG/Attribute/stroke-dasharray>`_.

        :return: corresponding svg attribute :code:`stroke-dasharray`
        :rtype: str
        """
        if not hasattr(self, 'linestyle') and not hasattr(self, 'linestyle_ext'):
            logger.error("Object must have either 'linestyle' or 'linestyle_ext' attribute")

        # Determine line style
        style_value = getattr(self, 'linestyle', getattr(self, 'linestyle_ext')).to_int()
        
        if style_value == 1:  # Dotted
            return "4,10"
        elif style_value == 2:  # Dashed
            return "1,10"
        elif style_value == 3:  # Dash-dotted
            return "1,10,4,10"
        else:  # Solid
            return "none"
           
    def get_svg_arc_path(self, center, radius_x, radius_y, angle_start, angle_end) -> str:
        """
        This function returns the svg path data for an arc.
    
        :param tuple center: The center coordinates of the arc
        :param int radius_x: The x-radius of the arc
        :param int radius_y: The y-radius of the arc
        :param float angle_start: The start angle of the arc
        :param float angle_end: The end angle of the arc.
    
        :return: corresponding svg path data for arc
        :rtype: str
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
            
