from pyaltiumlib.pcblib.records.base import _GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader, Coordinate, CoordinatePoint

class PcbTrack(_GenericPCBRecord):
    
    def __init__(self, parent, stream):
        
        super().__init__(parent)
        
        self.parse( stream )
    
        
    def __repr__(self):
        return f"PCBTack"
    
    
    def parse(self, stream):
        
        block = BinaryReader.from_stream( stream )
        
        # Read Block 
        if block.has_content():
            self.read_common( block.read(13) )
            self.start = block.read_bin_coord()
            self.end = block.read_bin_coord() 
            self.linewidth = Coordinate.parse_bin( block.read(4) )   
        
# =============================================================================
#     Drawing related
# ============================================================================= 
       
    def get_bounding_box(self):
        """
        Return bounding box for the object
        """
        
        half_width = float(self.linewidth) / 2
        
        min_x = min(float(self.start.x), float(self.end.x)) - half_width
        min_y = min(float(self.start.y), float(self.end.y)) - half_width
        max_x = max(float(self.start.x), float(self.end.x)) + half_width
        max_y = max(float(self.start.y), float(self.end.y)) + half_width
        
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

        start = (self.start * zoom) + offset
        end = (self.end * zoom) + offset
        
        layer = self.get_layer_by_id(self.layer)
            
        dwg.add(dwg.line(start = start.get_int(),
                         end = end.get_int(),
                         stroke = layer.color.to_hex(),
                         stroke_width = int(self.linewidth) * zoom,
                         stroke_linejoin="round",
                         stroke_linecap="round"
                         ))