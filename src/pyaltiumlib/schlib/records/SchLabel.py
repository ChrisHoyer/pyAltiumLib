from pyaltiumlib.schlib.records.base import _SchCommonParam
from pyaltiumlib.datatypes import SchematicTextOrientation, SchematicTextJustification

class SchLabel(_SchCommonParam):
    
    def __init__(self, data, parent):
       
        super().__init__(data, parent)
        
        if not( self.record == 4 ):
            raise TypeError("Incorrect assigned schematic record")
            
        self.orientation = SchematicTextOrientation( self.rawdata.get("orientation", 0))
        self.justification = SchematicTextJustification( self.rawdata.get("justification", 0))
        
        self.font_id = int(self.rawdata.get("fontid", 0))
        self.text = self.rawdata.get("text", "")
        self.is_mirrored = self.rawdata.get_bool('ismirrored')
        self.is_hidden = self.rawdata.get_bool('ishidden')
            

    def __repr__(self):
        return f"SchLabel "        
        
# =============================================================================
#     Drawing related
# =============================================================================   

    def get_bounding_box(self):
        """
        Return bounding box for the object
        """

        self.alignment = {
            "vertical": self.justification.get_vertical(),
            "horizontal": self.justification.get_horizontal(),
            "rotation": self.orientation.to_int() * -90,
            "position" : self.location.copy()
            }

        # Estimate text size
        width = len(self.text) * self.Symbol.LibFile._Fonts[self.font_id].size * 0.6
        height = self.Symbol.LibFile._Fonts[self.font_id].size

        end = self.location.copy()
        start = self.location.copy()

        # Rotation
        if self.orientation.to_int() == 0:
            end.x = end.x + width
            end.y = end.y - height 
            
        if self.orientation.to_int() == 1:
            start.x = start.x - height
            end.y = end.y - width  

        if self.orientation.to_int() == 2:
            start.x = start.x - width
            start.y = start.y + height
                
        if self.orientation.to_int() == 3:
            end.x = end.x - height
            start.y = start.y + width 

        return [start, end]


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
                
        insert = (self.location * zoom) + offset
        
        dwg.add(dwg.text(self.text,
                         font_size = self.Symbol.LibFile._Fonts[self.font_id].size * zoom,
                         font_family = self.Symbol.LibFile._Fonts[self.font_id].font,
                         font_weight = self.Symbol.LibFile._Fonts[self.font_id].bold,
                         font_style = self.Symbol.LibFile._Fonts[self.font_id].style,
                         text_decoration = self.Symbol.LibFile._Fonts[self.font_id].text_decoration, 
                         insert = insert.get_int(),
                         fill = self.color.to_hex(),
                         dominant_baseline=self.alignment["vertical"],
                         text_anchor=self.alignment["horizontal"],
                         transform=f"rotate({self.alignment['rotation']} {int(insert.x)} {int(insert.y)})"
                         ))
        

        return None
