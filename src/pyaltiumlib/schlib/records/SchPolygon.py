from pyaltiumlib.schlib.records.base import _SchCommonParam
from pyaltiumlib.datatypes import SchCoord, SchCoordPoint, SchematicLineWidth

class SchPolygon(_SchCommonParam):
    
    def __init__(self, data, parent):
       
        super().__init__(data, parent)
        
        if not( self.record == 7 ):
            raise TypeError("Incorrect assigned schematic record")

        self.transparent = self.rawdata.get_bool("transparent")
        self.issolid = self.rawdata.get_bool("issolid")
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))  
            
        self.num_vertices = int( self.rawdata.get('locationcount', 0) )        
        self.vertices = []
        for i in range(self.num_vertices):
            
            xy = SchCoordPoint(SchCoord.parse_dpx(f"x{i+1}", self.rawdata),
                                SchCoord.parse_dpx(f"y{i+1}", self.rawdata, scale=-1.0))
            
            self.vertices.append( xy )
                       
             
        
    def __repr__(self):
        return f"SchPolygon "        
        
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

        return [SchCoordPoint(SchCoord(min_x), SchCoord(min_y)),
                SchCoordPoint(SchCoord(max_x), SchCoord(max_y))]

    
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
        for vertex in self.vertices:
            points.append( (vertex * zoom) + offset )
        # Close Polygon
        points.append( points[0] )
                
        dwg.add(dwg.polyline( [x.get_int() for x in points],
                             fill = self.areacolor.to_hex() if self.issolid else "none",
                             stroke = self.color.to_hex(),
                             stroke_width = int(self.linewidth),
                             stroke_linejoin="round",
                             stroke_linecap="round"
                             ))
        

    



