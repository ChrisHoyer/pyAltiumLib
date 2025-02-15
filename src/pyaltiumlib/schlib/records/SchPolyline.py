from pyaltiumlib.schlib.records.base import GenericSchRecord
from pyaltiumlib.datatypes import SchematicLineWidth, SchematicLineStyle, SchematicLineShape
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint

from typing import Tuple

# Set up logging
import logging
logger = logging.getLogger(__name__)

class SchPolyline(GenericSchRecord):
    """
    Implementation of a schematic record
    See also :ref:`SchPrimitive06` details on this schematic records. This record can be drawn.
    
    :param Dict data: Dictionary containing raw record data
    :param class parent: Parent symbol object  
    :raises ValueError: If record id is not valid
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 6:
            logger.warning(f"Error in mapping between record objects and record id! - incorrect id {self.record}")

        self.transparent = self.rawdata.get_bool("transparent")
        self.issolid = self.rawdata.get_bool("issolid")
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))  
            
        self.num_vertices = int(self.rawdata.get('locationcount', 0))
        
        self.vertices = []
        for i in range(self.num_vertices):
            xy = CoordinatePoint(Coordinate.parse_dpx(f"x{i+1}", self.rawdata),
                                Coordinate.parse_dpx(f"y{i+1}", self.rawdata, scale=-1.0))
            self.vertices.append(xy)
                       
        self.linestyle = SchematicLineStyle(self.rawdata.get('linestyle', 0))
        self.linestyle_ext = SchematicLineStyle(self.rawdata.get('linestyleext', 0))
        self.lineshape_start = SchematicLineShape(self.rawdata.get('startlineshape', 0))            
        self.lineshape_end = SchematicLineShape(self.rawdata.get('endlineshape', 0))  
        self.lineshape_size = SchematicLineWidth(self.rawdata.get('lineshapesize', 0))

        self.is_drawable = True           
        
    def get_bounding_box(self) -> Tuple[CoordinatePoint, CoordinatePoint]:
        """
        Generates and returns a bounding box for this record
        
        :return: List with two coordinate entries 
        :rtype: tuple with :ref:`DataTypeCoordinatePoint`
        """
        min_x = float("inf")
        min_y = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")
    
        min_x = min(min_x, float(self.location.x))
        min_y = min(min_y, float(self.location.y))
        max_x = max(max_x, float(self.location.x))
        max_y = max(max_y, float(self.location.y))
        
        for vertex in self.vertices:
            min_x = min(min_x, float(vertex.x))
            min_y = min(min_y, float(vertex.y))
            max_x = max(max_x, float(vertex.x))
            max_y = max(max_y, float(vertex.y))

        return [CoordinatePoint(Coordinate(min_x), Coordinate(min_y)),
                CoordinatePoint(Coordinate(max_x), Coordinate(max_y))]

    def draw_svg(self, dwg, offset, zoom) -> None:
        """
        Draw schematic record using svgwrite.
        
        :param graphic dwg: svg drawing object
        :param CoordinatePoint offset: Move drawing by the given offset as :ref:`DataTypeCoordinatePoint`
        :param float zoom: Scaling Factor for all elements  
        """
        points = []
        for vertex in self.vertices:
            points.append((vertex * zoom) + offset)

        line = dwg.add(dwg.polyline([x.to_int_tuple() for x in points],
                             fill="none",
                             stroke_dasharray=self.get_svg_stroke_dasharray(),
                             stroke=self.color.to_hex(),
                             stroke_width=int(self.linewidth) * zoom,
                             stroke_linejoin="round",
                             stroke_linecap="round"))

        # Add the marker to the drawing
        marker_start = self.lineshape_start.draw_marker(dwg, int(self.lineshape_size) * zoom,
                                                        self.color.to_hex())        
        marker_end = self.lineshape_end.draw_marker(dwg, int(self.lineshape_size) * zoom,
                                                    self.color.to_hex(), end=True)
        
        line.set_markers((marker_start, False, marker_end))