from pyaltiumlib.schlib.records.base import _SchCommonParam


class SchDesignator(_SchCommonParam):
    
    def __init__(self, data, parent):
       
        super().__init__(data, parent)
        
        if not( self.record == 34 ):
            raise TypeError("Incorrect assigned schematic record")
            
            
            
        
    def __repr__(self):
        return f"SchDesignator "        
        
# =============================================================================
#     Drawing related
# =============================================================================   
         
    def get_bounding_box(self):
        """
        Return bounding box for the object
        """
        
        return None

    
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

        return None
        
    



