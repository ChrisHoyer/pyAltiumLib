from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint

# Configure logging
import logging
logger = logging.getLogger(__name__)

class BinaryReader:
    """
    A utility class for reading binary data with structured methods.
    
    :param bytes data: The binary data to be read.
    """    
    def __init__(self, data):
        self.data = data
        self.offset = 0

    @classmethod        
    def from_stream(cls, stream, size_length=4):
        """
        Reads a binary block from a stream and initializes a BinaryReader.
        
        :param file-like object stream: The binary stream to read from.
        :param int optional size_length: Number of bytes indicating the block size.
        :return: An instance of BinaryReader.
        :rtype: BinaryReader
        """
        length = int.from_bytes( stream.read( size_length ), "little" )
        data = stream.read( length )
        
        if len(data) != length:
             logger.warning("Stream does not match the declared block length.")        
        
        return cls( data )       

    def has_content(self):
        """
        Checks if there is remaining data to read.
        
        :return: True if data exists, False otherwise.
        :rtype: bool
        """
        return not len(self.data) == 0
    
    def length(self):
        """
        Returns the length of the binary data.
        
        :return: The length of the data.
        :rtype: int
        """
        return len(self.data)
        
    def read(self, length):
        """
        Reads a specified number of bytes from the binary data.
        
        :param int length: The number of bytes to read.
        :return: The read bytes.
        :rtype: bytes
        """                    
        if self.offset + length > len(self.data):
            logger.warning("Not enough data to read the requested length.")
        
        result = self.data[self.offset:self.offset + length]
        self.offset += length
        return result       

    def read_byte(self):
        """
        Reads a single byte from the binary data.
        
        :return: The read byte.
        :rtype: bytes
        """
        return self.read(1)

    def read_int8(self, signed=False):
        """
        Reads an 8-bit integer.
        
        :param bool optional signed: Whether to interpret the value as signed.
        :return: The integer value.
        :rtype: int
        """
        return int.from_bytes(self.read_byte(), signed=signed)
    
    def read_int16(self, signed=False):
        """
        Reads a 16-bit integer.
        
        :param bool optional signed: Whether to interpret the value as signed.
        :return: The integer value.
        :rtype: int
        """
        return int.from_bytes(self.read(2), byteorder="little", signed=signed)
    
    def read_int32(self, signed=False):
        """
        Reads a 32-bit integer.
        
        :param bool optional signed: Whether to interpret the value as signed.
        :return: The integer value.
        :rtype: int
        """
        return int.from_bytes(self.read(4), byteorder="little", signed=signed)

    def read_double(self):
        """
        Reads an IEEE 754 double-precision floating point value.
        
        :return: The double value.
        :rtype: float
        """
        value = int.from_bytes(self.read(8), byteorder='little', signed=False)
        sign = (value >> 63) & 0x1
        exponent = (value >> 52) & 0x7FF
        mantissa = value & ((1 << 52) - 1)

        if exponent == 0x7FF:
            return float('inf') if mantissa == 0 else float('nan')

        if exponent == 0:
            result = (mantissa / (1 << 52)) * (2 ** (-1022))
        else:
            result = (1 + (mantissa / (1 << 52))) * (2 ** (exponent - 1023))

        return -result if sign == 1 else result

    def read_string_block(self, size_string=1):
        """
        Reads a length-prefixed string.
        
        :param int optional size_string: Number of bytes specifying the string length.
        
        :return: The decoded string.
        :rtype: str
        """
        length_string = int.from_bytes(self.read(size_string), "little")
        string_data = self.read( length_string )
                 
        if len(string_data) != length_string:
            logger.warning("String does not match the declared string length.")        
        
        return string_data.decode('windows-1252')

    def read_bin_coord(self, scaley=-1.0, double=False, double_scaling = 1/10000.0):
        """
        Reads a binary coordinate pair and returns a CoordinatePoint.
        
        :param float scaley: Scaling factor for the Y coordinate.
        :param bool optional double: Read coordinates as double
        :param float optional float: Scaling of double values
        
        :return: A CoordinatePoint object.
        :rtype: CoordinatePoint
        """
        if double:
            x = (self.read_double() * double_scaling)
            y = (self.read_double() * double_scaling) * scaley
            return CoordinatePoint( Coordinate(x), Coordinate(y))  
        
        else:
            x = self.read(4)
            y = self.read(4)
            return CoordinatePoint( Coordinate.parse_bin(x), Coordinate.parse_bin(y, scale=scaley))  

    def read_unicode_text(self, length=32, encoding='utf-16-le'):
        """
        Reads a Unicode string of fixed length.
        
        :param int optional length: Maximum length of the string in bytes.
        :param str optional encoding: The encoding format.
        
        :return: The decoded Unicode string.
        :rtype: str
        """
        pos = self.offset
        data = []
        while len(data) < length:
            
            if self.offset + 2 > len(self.data):
                logger.warning("Not enough data to read.")
                
            unicode_char = self.read(2)
            if unicode_char == b'\x00\x00':  # Null terminator
                break
            data.extend(unicode_char)
            
        # Ensure we skip the remaining bytes to read exactly `length` bytes
        self.offset = pos + length
        
        return bytes(data).decode(encoding)

