"""
Schematic Data Types for Records
"""
class SchCoord:
    def __init__(self, value):
        self.value = value
        
    @classmethod
    def parse_dpx(cls, key, data, scale=1.0):        
        num = int(data.get(key, 0))
        frac = int(data.get(key + "_frac", 0))
        
        coord = (num * 10.0 + frac / 10000.0)
        
        return cls( scale * coord/10 )
        
    def __repr__(self):
        return f"{self.value}"       

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return SchCoord(self.value * other)
        elif isinstance(other, SchCoord):
            return SchCoord(self.value * other.value)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return SchCoord(self.value + other)
        elif isinstance(other, SchCoord):
            return SchCoord(self.value + other.value)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return SchCoord(self.value - other)
        elif isinstance(other, SchCoord):
            return SchCoord(self.value - other.value)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __rsub__(self, other):
        return self.__sub__(other)

    def __lt__(self, other):
        if isinstance(other, SchCoord):
            return self.value < other.value
        elif isinstance(other, (int, float)):
            return self.value < other
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, SchCoord):
            return self.value > other.value
        elif isinstance(other, (int, float)):
            return self.value > other
        return NotImplemented

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other
  

class SchCoordPoint:
    def __init__(self, x, y):
        if not isinstance(x, SchCoord):
            x = SchCoord(x)
        if not isinstance(y, SchCoord):
            y = SchCoord(y)
            
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x};{self.y})"    

    def __add__(self, other):
        if isinstance(other, SchCoordPoint):
            return SchCoordPoint(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, SchCoordPoint):
            return SchCoordPoint(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return SchCoordPoint(self.x * other, self.y * other)
        elif isinstance(other, SchCoordPoint):
            return SchCoordPoint(self.x * other.x, self.y * other.y)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __rsub__(self, other):
        return self.__sub__(other)

    def copy(self):
        return SchCoordPoint(self.x, self.y)