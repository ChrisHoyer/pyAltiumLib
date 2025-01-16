class ParameterColor:
    
    def __init__(self, color):
        """
        Initializes the color from an integer representing the BGR value.
        :param color: The BGR color in 0xBBGGRR format.
        """
        
        self.color = int(color)
        
        self.blue = (self.color >> 16) & 0xFF
        self.green = (self.color >> 8) & 0xFF
        self.red = self.color & 0xFF 
        
    @classmethod
    def from_hex(cls, hex_color):
        
        if not hex_color.startswith("#") or len(hex_color) != 7:
            raise ValueError("Invalid hex color format. Expected format: #RRGGBB")

        return cls( int( f"{hex_color[5:7]}{hex_color[3:5]}{hex_color[1:3]}", 16) )
        
    def __repr__(self):
        return f"{self.color}"          
        
    def to_hex(self):
        return f"#{self.red:02X}{self.green:02X}{self.blue:02X}"
