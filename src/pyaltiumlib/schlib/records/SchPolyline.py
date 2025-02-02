from pyaltiumlib.schlib.records.base import _GenericSchRecord
from pyaltiumlib.datatypes import SchematicLineWidth, SchematicLineStyle, SchematicLineShape
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint
import logging

# Set up logging
logger = logging.getLogger(__name__)

class SchPolyline(_GenericSchRecord):
    """
    A class to represent a polyline in an Altium Schematic Library.

    Attributes:
        transparent (bool): Whether the polyline is transparent.
        issolid (bool): Whether the polyline is solid.
        linewidth (SchematicLineWidth): The width of the polyline.
        num_vertices (int): The number of vertices in the polyline.
        vertices (List[CoordinatePoint]): The vertices of the polyline.
        linestyle (SchematicLineStyle): The line style of the polyline.
        linestyle_ext (SchematicLineStyle): The extended line style of the polyline.
        lineshape_start (SchematicLineShape): The shape at the start of the polyline.
        lineshape_end (SchematicLineShape): The shape at the end of the polyline.
        lineshape_size (SchematicLineWidth): The size of the line shapes.
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 6:
            raise TypeError("Incorrect assigned schematic record")

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

        self.is_initialized = True           
        
    def __repr__(self):
        return f"SchPolyline"

    def get_bounding_box(self):
        """
        Return the bounding box for the polyline.

        Returns:
            List[CoordinatePoint]: The bounding box as a list of two CoordinatePoints.
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

    def draw_svg(self, dwg, offset, zoom):
        """
        Draw the polyline using svgwrite.

        Args:
            dwg: The SVG drawing object.
            offset (CoordinatePoint): The offset for drawing.
            zoom (float): The zoom factor for scaling.
        """
        points = []
        for vertex in self.vertices:
            points.append((vertex * zoom) + offset)

        line = dwg.add(dwg.polyline([x.to_int_tuple() for x in points],
                             fill="none",
                             stroke_dasharray=self.draw_linestyle(),
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