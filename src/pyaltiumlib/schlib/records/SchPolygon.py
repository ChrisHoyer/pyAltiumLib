from pyaltiumlib.schlib.records.base import GenericSchRecord
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint
from pyaltiumlib.datatypes import SchematicLineWidth

from typing import List, Tuple

# Configure logging
import logging
logger = logging.getLogger(__name__)

class SchPolygon(GenericSchRecord):
    """
    Implementation of a schematic record
    See also :ref:`SchPrimitive07` details on this schematic records. This record can be drawn.
    
    :param Dict data: Dictionary containing raw record data
    :param class parent: Parent symbol object  
    :raises ValueError: If record id is not valid
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 7:
            logger.warning(f"Error in mapping between record objects and record id! - incorrect id {self.record}")
           
        self.transparent = self.rawdata.get_bool("transparent", 0)
        self.issolid = self.rawdata.get_bool("issolid", 0)
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))
        
        self.num_vertices = int(self.rawdata.get('locationcount', 0))
        self.vertices = self._parse_vertices()
        
        self.is_drawable = True

    def _parse_vertices(self) -> List[CoordinatePoint]:
        vertices = []
        for i in range(self.num_vertices):
            try:
                x = Coordinate.parse_dpx(f"x{i+1}", self.rawdata)
                y = Coordinate.parse_dpx(f"y{i+1}", self.rawdata, scale=-1.0)
                vertices.append(CoordinatePoint(x, y))
            except Exception as e:
                logger.error(f"Failed to parse vertex {i+1}: {str(e)}")
                
        return vertices

    def get_bounding_box(self) -> Tuple[CoordinatePoint, CoordinatePoint]:
        """
        Generates and returns a bounding box for this record
        
        :return: List with two coordinate entries 
        :rtype: tuple with :ref:`DataTypeCoordinatePoint`
        """
        if not self.vertices:
            return self.location, self.location

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
        
    def draw_svg(self, dwg, offset: CoordinatePoint, zoom: float) -> None:
        """
        Draw schematic record using svgwrite.
        
        :param graphic dwg: svg drawing object
        :param CoordinatePoint offset: Move drawing by the given offset as :ref:`DataTypeCoordinatePoint`
        :param float zoom: Scaling Factor for all elements  
        """
        if not self.vertices:
            logger.warning("No vertices found for polygon, skipping draw")
            return

        try:

            points = [(vertex * zoom + offset).to_int_tuple() for vertex in self.vertices]
            points.append(points[0])

            dwg.add(dwg.polyline(
                points=points,
                fill=self.areacolor.to_hex() if self.issolid else "none",
                stroke=self.color.to_hex(),
                stroke_width=int(self.linewidth) * zoom,
                stroke_linejoin="round",
                stroke_linecap="round"
            ))
        except Exception as e:
            logger.error(f"Failed to draw polygon: {str(e)}")