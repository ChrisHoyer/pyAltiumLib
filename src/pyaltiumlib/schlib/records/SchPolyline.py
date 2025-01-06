from pyaltiumlib.schlib.records.base import _SchCommonParam
from pyaltiumlib.datatypes import ( SchCoord, SchCoordPoint, 
                                   SchematicLineWidth, SchematicLineStyle, 
                                   SchematicLineShape )
from ._render_helpers import draw_dashed_line

class SchPolyline(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 6 ):
            raise TypeError("Incorrect assigned schematic record")

        self.transparent = bool( self.rawdata.get("transparent", "F").upper() == "T" )
        self.issolid = bool( self.rawdata.get("issolid", "F").upper() == "T" )
        self.linewidth = SchematicLineWidth(self.rawdata.get('linewidth', 0))  
            
        self.num_vertices = int( self.rawdata.get('locationcount', 0) )
        
        self.vertices = []
        for i in range(self.num_vertices):
            
            xy = SchCoordPoint(SchCoord.parse_dpx(f"x{i+1}", self.rawdata),
                                SchCoord.parse_dpx(f"y{i+1}", self.rawdata, scale=-1.0))
            
            self.vertices.append( xy )
                       
        self.linestyle = SchematicLineStyle(self.rawdata.get('linestyle', 0))
        self.lineshape_start = SchematicLineShape(self.rawdata.get('startlineshape', 0))            
        self.lineshape_end = SchematicLineShape(self.rawdata.get('endlineshape', 0))  
        self.lineshape_size = self.rawdata.get('lineshapesize', 0)              
        
    def __repr__(self):
        return f"SchPolyline "        
        
# =============================================================================
#     Drawing related
# =============================================================================   
         
    def get_bounding_box(self):
        """
        Return bounding box for the object, including all coordinates from
        self.location and self.vertices.
        """
        min_x = float("inf")
        min_y = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")
    
        min_x = min(min_x, float(self.location.x))
        min_y = min(min_y, float(self.location.y))
        max_x = max(max_x, float(self.location.x))
        max_y = max(max_y, float(self.location.y))
        
        # print( )
        # print( self.rawdata )
        # print( )
        
        # print("SchPolyline - BoundingBox")
        # print(f"Start: {self.location}")
    
        for vertex in self.vertices:
            min_x = min(min_x, float(vertex.x))
            min_y = min(min_y, float(vertex.y))
            max_x = max(max_x, float(vertex.x))
            max_y = max(max_y, float(vertex.y))
            
            # print(f"Vertex: {vertex}")
    
        # print(f"Bounding: {min_x};{min_y} - {max_x};{max_y}")

        return [SchCoordPoint(SchCoord(min_x), SchCoord(min_y)),
                SchCoordPoint(SchCoord(max_x), SchCoord(max_y))]


    
    def draw(self, graphic, offset, zoom):
        """
        Draw Element using ImageDraw Module of Pillow with support for zoom and offsetting.
        """

        scaled_vertices = []
        for vertex in self.vertices:
            loc_x = (vertex.x * zoom) + offset.x
            loc_y = (vertex.y * zoom) + offset.y
            scaled_vertices.append((float(loc_x), float(loc_y)))
    
        if self.linestyle.to_int():
            for i in range(len(scaled_vertices) - 1):
               start = scaled_vertices[i]
               end = scaled_vertices[i + 1]
               draw_dashed_line(graphic, start, end, self.color.to_hex(), int(self.linewidth))
               
        else:
            graphic.line(scaled_vertices,
                         fill=self.color.to_hex(),
                         width=int(self.linewidth))
        

    



