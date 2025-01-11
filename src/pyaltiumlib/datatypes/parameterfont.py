class ParameterFont:
    
    def __init__(self, font, size, bold=False, italic=False,
                 underline=False, strikeout=False):

        self.font = font
        self.size = float(size)
        
        self.bold = "bold" if bold else "normal"
        self.style = "italic" if italic else "normal"
        
        self.text_decoration = 'underline' if underline else ''
        if strikeout:
            self.text_decoration += ' line-through' if self.text_decoration else 'line-through'

    def __repr__(self):
        return f"{self.font}"          
        

