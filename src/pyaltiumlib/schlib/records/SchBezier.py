from pyaltiumlib.schlib.records.base import _GenericSchRecord
from pyaltiumlib.datatypes import SchematicLineWidth, SchematicLineStyle
from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint

class SchBezier(_GenericSchRecord):
    
    def __init__(self, data, parent):
       
        super().__init__(data, parent)
        
        if not( self.record == 5 ):
            raise TypeError("Incorrect assigned schematic record")

        self.transparent = self.rawdata.get_bool("transparent")
        self.issolid = self.rawdata.get_bool("issolid")
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))  
            
        self.num_vertices = int( self.rawdata.get('locationcount', 0) )
        
        self.vertices = []
        for i in range(self.num_vertices):
            
            xy = CoordinatePoint(Coordinate.parse_dpx(f"x{i+1}", self.rawdata),
                                 Coordinate.parse_dpx(f"y{i+1}", self.rawdata, scale=-1.0))
            
            self.vertices.append( xy )
                       
        self.linestyle = SchematicLineStyle(self.rawdata.get('linestyle', 0))
        self.linestyle_ext = SchematicLineStyle(self.rawdata.get('linestyleext', 0))
      
        
    def __repr__(self):
        return f"SchBezier "        
        
# =============================================================================
#     Drawing related
# ============================================================================= 
  
    def get_bounding_box(self):
        """
        Return bounding box for the object
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
        Draw element using svgwrite
        Args:
            dwg: svg Drawing
            offset (int): SchematicCoordinate with drawing center point
            zoom (float): Scaling Factor for all elements
        Returns:
            None
        """

        points = []
        #points.append( (self.location * zoom) + offset )
        for vertex in self.vertices:
            points.append( (vertex * zoom) + offset )
            
        points = [x.to_int_tuple() for x in points]
        interp_points = self.bezier_interpolate(points, steps=100)

            
        dwg.add(dwg.polyline(interp_points,
                             fill = "none",
                             stroke_dasharray = self.draw_linestyle(),
                             stroke = self.color.to_hex(),
                             stroke_width = int(self.linewidth) * zoom,
                             stroke_linejoin="round",
                             stroke_linecap="round"
                             ))
        
    
    
    def bezier_interpolate(self, control_points, steps=20):
        interpolated_points = []
        
        # Bezier curve using De Casteljau's algorithm
        for t in range(steps + 1):
            t /= steps
            points = control_points[:]
            while len(points) > 1:
                points = [
                    (
                        (1 - t) * p0[0] + t * p1[0],
                        (1 - t) * p0[1] + t * p1[1],
                    )
                    for p0, p1 in zip(points[:-1], points[1:])
                ]
            interpolated_points.append(points[0])
    
        return interpolated_points


