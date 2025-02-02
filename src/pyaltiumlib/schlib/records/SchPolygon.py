from pyaltiumlib.schlib.records.base import _GenericSchRecord
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint
from pyaltiumlib.datatypes import SchematicLineWidth
import logging
from typing import List, Tuple

# Configure logging
logger = logging.getLogger(__name__)

class SchPolygon(_GenericSchRecord):
    """
    Represents a polygon in an Altium schematic library.
    
    Attributes:
        transparent (bool): Whether the polygon is transparent.
        issolid (bool): Whether the polygon is filled.
        linewidth (SchematicLineWidth): The width of the polygon's border.
        num_vertices (int): The number of vertices in the polygon.
        vertices (List[CoordinatePoint]): The vertices of the polygon.
    """

    def __init__(self, data, parent):
        """Initialize the polygon with data validation."""
        super().__init__(data, parent)
        
        if self.record != 7:
            raise ValueError(f"Invalid record type {self.record} for SchPolygon (expected 7)")
            
        self.transparent = self.rawdata.get_bool("transparent", 0)
        self.issolid = self.rawdata.get_bool("issolid", 0)
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))
        
        self.num_vertices = int(self.rawdata.get('locationcount', 0))
        self.vertices = self._parse_vertices()
        
        self.is_initialized = True

    def __repr__(self) -> str:
        """Return a string representation of the polygon."""
        return f"SchPolygon(vertices={self.num_vertices}, solid={self.issolid})"

    def _parse_vertices(self) -> List[CoordinatePoint]:
        """Parse and validate polygon vertices."""
        vertices = []
        for i in range(self.num_vertices):
            try:
                x = Coordinate.parse_dpx(f"x{i+1}", self.rawdata)
                y = Coordinate.parse_dpx(f"y{i+1}", self.rawdata, scale=-1.0)
                vertices.append(CoordinatePoint(x, y))
            except Exception as e:
                logger.error(f"Failed to parse vertex {i+1}: {str(e)}")
                raise ValueError(f"Invalid vertex data at index {i+1}")
                
        return vertices

    def get_bounding_box(self) -> Tuple[CoordinatePoint, CoordinatePoint]:
        """
        Calculate the bounding box for the polygon.
        
        Returns:
            Tuple[CoordinatePoint, CoordinatePoint]: The min and max points of the bounding box.
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
        Render the polygon to an SVG drawing.
        
        Args:
            dwg: The SVG drawing object.
            offset (CoordinatePoint): The offset for drawing.
            zoom (float): The zoom factor for scaling.
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