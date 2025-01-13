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

    def read_int8(self):
        return int.from_bytes(self.read_byte())
    
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

    def read_string_block(self, size_string=1):
        
        length_string = int.from_bytes( self.read( size_string ), "little" )
        string_data = self.read( length_string )
                 
        if len(string_data) != length_string:
            raise ValueError("String does not match the declared string length.")        
        
        return string_data.decode('windows-1252')

    def read_bin_coord(self):
        x = self.read(4)
        y = self.read(4)
        return CoordinatePoint( Coordinate.parse_bin(x), Coordinate.parse_bin(y))      
