from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint

class BinaryReader:
    
    def __init__(self, data):
        self.data = data
        self.offset = 0

    @classmethod        
    def from_stream(cls, stream, size_length=4):
        length = int.from_bytes( stream.read( size_length ), "little" )
        data = stream.read( length )
        
        if len(data) != length:
            raise ValueError("Stream does not match the declared block length.")        
        
        return cls( data )       

    def has_content(self):
        return not len(self.data) == 0
    
    def length(self):
        return len(self.data)
        
    def read(self, length):
                    
        if self.offset + length > len(self.data):
            raise ValueError("Not enough data to read the requested length.")
        
        result = self.data[self.offset:self.offset + length]
        self.offset += length
        return result        

    def read_byte(self):
        if self.offset + 1 > len(self.data):
            raise ValueError("Not enough data to read.")
        return self.read(1)

    def read_int8(self, signed=False):
        return int.from_bytes(self.read_byte(), signed=signed)
    
    def read_int16(self, signed=False):
        if self.offset + 2 > len(self.data):
            raise ValueError("Not enough data to read an Int16.")
        
        value = int.from_bytes(self.data[self.offset:self.offset + 2], byteorder="little", signed=signed)
        self.offset += 2
        return value
    
    def read_int32(self, signed=False):
        if self.offset + 4 > len(self.data):
            raise ValueError("Not enough data to read an Int32.")
        
        value = int.from_bytes(self.data[self.offset:self.offset + 4], byteorder="little", signed=signed)
        self.offset += 4
        return value

    def read_double(self):
        if self.offset + 8 > len(self.data):
            raise ValueError("Not enough data to read a Double.")

        raw_bytes = self.data[self.offset:self.offset + 8]
        self.offset += 8
        return self._decode_double(raw_bytes)

    def read_string_block(self, size_string=1):
        
        length_string = int.from_bytes( self.read( size_string ), "little" )
        string_data = self.read( length_string )
                 
        if len(string_data) != length_string:
            raise ValueError("String does not match the declared string length.")        
        
        return string_data.decode('windows-1252')

    def read_bin_coord(self, scaley=-1.0):
        x = self.read(4)
        y = self.read(4)
        return CoordinatePoint( Coordinate.parse_bin(x), Coordinate.parse_bin(y, scale=scaley)) 

    def read_unicode_text(self, length=32, encoding='utf-16-le'):
        
        pos = self.offset
        data = []
    
        while len(data) < length:
            if self.offset + 2 > len(self.data):
                raise ValueError("Not enough data to read.")
            
            # Read 2 bytes (1 Unicode character)
            unicode_char = self.read(2)
            if unicode_char == b'\x00\x00':  # Null terminator
                break
            data.extend(unicode_char)
        
        # Ensure we skip the remaining bytes to read exactly `length` bytes
        self.offset = pos + length
        
        return bytes(data).decode(encoding)
    
    
# =================================0

    def _decode_double(self, raw_bytes):
        # Decode IEEE 754 double-precision format
        value = 0
        for i, b in enumerate(raw_bytes):
            value |= b << (i * 8)

        sign = (value >> 63) & 0x1
        exponent = (value >> 52) & 0x7FF
        mantissa = value & ((1 << 52) - 1)

        if exponent == 0x7FF:
            if mantissa == 0:
                return float('inf') if sign == 0 else float('-inf')
            return float('nan')

        if exponent == 0:
            result = (mantissa / (1 << 52)) * (2 ** (-1022))
        else:
            result = (1 + (mantissa / (1 << 52))) * (2 ** (exponent - 1023))

        return -result if sign == 1 else result

