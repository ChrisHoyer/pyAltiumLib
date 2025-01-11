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
        
    def __repr__(self):
        return f"{self.color}"          
        
    def to_hex(self):
        return f"#{self.red:02X}{self.green:02X}{self.blue:02X}"
