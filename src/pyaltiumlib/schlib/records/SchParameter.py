from pyaltiumlib.schlib.records.base import _GenericSchRecord


class SchParameter(_GenericSchRecord):
    
    def __init__(self, data, parent):
       
        super().__init__(data, parent)
        
        if not( self.record == 41 ):
            raise TypeError("Incorrect assigned schematic record")
            

    def __repr__(self):
        return f"SchParameter "        
  
        
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



