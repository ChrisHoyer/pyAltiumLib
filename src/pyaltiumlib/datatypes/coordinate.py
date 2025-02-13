import math

# Set up logging
import logging
logger = logging.getLogger(__name__)

class Coordinate:
    """
    Represents a single coordinate value.

    This class provides parsing functions for extracting coordinates from
    different data formats, as well as mathematical operations.

    :param value: The numerical value of the coordinate.
    :type value: int or float


    **Operations:**
    
    Supports addition, subtraction, multiplication, and division with both
    integers, floats, and other `Coordinate` instances. Can be compared 
    using `<`, `>`, `<=`, `>=` with both `Coordinate` instances and numerical values.
    """

    def __init__(self, value):
        self.value = value

    @classmethod
    def parse_dpx(cls, key, data, scale=1.0):
        """
        Parses a coordinate from a parameter collection data dictionary (schematic file).

        :param str key: The key corresponding to the coordinate.
        :param dict data: The dictionary containing coordinate data.
        :param float, optional scale: Scaling factor for the parsed coordinate.

        :return: A Coordinate instance with the parsed value.
        :rtype: Coordinate
        """
        num = int(data.get(key, 0))
        frac = int(data.get(key + "_frac", 0))
        coord = (num * 10.0 + frac / 10000.0)
        return cls(scale * coord / 10)

    @classmethod
    def parse_bin(cls, x_bytes, scale=1.0):
        """
        Parses a coordinate from binary data (pcb file).

        :param bytes x_bytes: Binary representation of the coordinate.
        :param float, optional scale: Scaling factor for the parsed coordinate.

        :return: A Coordinate instance with the parsed value.
        :rtype: Coordinate
        """
        x = int.from_bytes(x_bytes, byteorder="little", signed=True)
        return cls(scale * x / 10000.0)

    def __repr__(self):
        """Returns a string representation of the coordinate."""
        return f"{self.value}"

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)

# ================== Math Functions =========================================

    def __abs__(self):
        return abs(int(self.value))

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                logger.warning("Division by zero is not allowed.")
                raise
            return Coordinate(self.value / other)

        elif isinstance(other, Coordinate):
            if other.value == 0:
                logger.warning("Division by zero is not allowed.")
                raise
            return Coordinate(self.value / other.value)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Coordinate(self.value * other)
        elif isinstance(other, Coordinate):
            return Coordinate(self.value * other.value)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Coordinate(self.value + other)
        elif isinstance(other, Coordinate):
            return Coordinate(self.value + other.value)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Coordinate(self.value - other)
        elif isinstance(other, Coordinate):
            return Coordinate(self.value - other.value)
        return NotImplemented

    def __rtruediv__(self, other):
        return self.__div__(other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __rsub__(self, other):
        return self.__sub__(other)
    
    def __lt__(self, other):
        if isinstance(other, Coordinate):
            return self.value < other.value
        elif isinstance(other, (int, float)):
            return self.value < other
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Coordinate):
            return self.value > other.value
        elif isinstance(other, (int, float)):
            return self.value > other
        return NotImplemented

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

# =============================================================================       
# =============================================================================
#     2D Coordinate Point
# =============================================================================   

class CoordinatePoint: 
    """    
    This class encapsulates two `Coordinate` instances for the X and Y axes.

    :param int, float, or Coordinate x: The X-coordinate value.
    :param int, float, or Coordinate y: The Y-coordinate value.

    **Mathematical Operations:**
    
    Supports addition, subtraction, multiplication, and division with
    `CoordinatePoint` instances or numerical values.
    """

    def __init__(self, x, y):
        if not isinstance(x, Coordinate):
            x = Coordinate(x)
        if not isinstance(y, Coordinate):
            y = Coordinate(y)
        self.x = x
        self.y = y

    def __repr__(self):
        """Returns a string representation of the coordinate point."""
        return f"({self.x};{self.y})"

    def to_int(self):
        """Converts the coordinate point to integer values."""
        return CoordinatePoint(int(self.x), int(self.y))

    def to_int_tuple(self):
        """Returns the coordinate point as a tuple of integers."""
        return int(self.x), int(self.y)

    def expand(self, size):
        """
        Expands the coordinate point by a given size.

        :param size: The amount to expand by.
        :type size: int, float, or Coordinate
        :return: A new expanded CoordinatePoint.
        :rtype: CoordinatePoint
        """
        if isinstance(size, (int, float)):
            return CoordinatePoint(self.x + size, self.y + size)
        if isinstance(size, (int, Coordinate)):
            return CoordinatePoint(self.x + size.value, self.y - size.value)

    def rotate(self, center, angle):
        """
        Rotates the coordinate point around a given center by an angle.

        :param center: The center point for rotation.
        :type center: CoordinatePoint
        :param angle: The rotation angle in degrees.
        :type angle: float
        :return: The rotated CoordinatePoint.
        :rtype: CoordinatePoint
        """
        theta = math.radians(angle)
        x_rel = self.x - center.x
        y_rel = self.y - center.y

        x_rot = x_rel * math.cos(theta) - y_rel * math.sin(theta)
        y_rot = x_rel * math.sin(theta) + y_rel * math.cos(theta)

        self.x = x_rot + center.x
        self.y = y_rot + center.y
        return self

    def offset(self, offset_x, offset_y):
        """
        Offsets the coordinate point by given values.

        :param offset_x: Offset for the X coordinate.
        :type offset_x: int or float
        :param offset_y: Offset for the Y coordinate.
        :type offset_y: int or float
        :return: The offset CoordinatePoint.
        :rtype: CoordinatePoint
        """
        self.x = self.x + offset_x
        self.y = self.y + offset_y
        return self

    def copy(self):
        """Returns a copy of the CoordinatePoint."""
        return CoordinatePoint(self.x, self.y)

# ================== Math Functions =========================================

    def __abs__(self):
        return CoordinatePoint( abs(self.x), abs(self.y))
    
    
    def __add__(self, other):
        if isinstance(other, CoordinatePoint):
            return CoordinatePoint(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, CoordinatePoint):
            return CoordinatePoint(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                logger.warning("Division by zero is not allowed.")
                raise
            return CoordinatePoint(self.x / other, self.y / other)
        elif isinstance(other, Coordinate):
            if other.value == 0:
                logger.warning("Division by zero is not allowed.")
                raise
            return  CoordinatePoint(self.x / other.x, self.y / other.y)
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return CoordinatePoint(self.x * other, self.y * other)
        elif isinstance(other, CoordinatePoint):
            return CoordinatePoint(self.x * other.x, self.y * other.y)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __rsub__(self, other):
        return self.__sub__(other)