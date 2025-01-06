
"""


"""
@staticmethod
def ReadBlock(olestream, sizelength = 4):
    """
    Represents a data structure containing the length of the block and the data.
    The first 4 bytes define the length of the block (little-endian).
    """        

    length = int.from_bytes( olestream.read( sizelength ), "little" )
    
    data = olestream.read( length )
    
    if len(data) != length:
        raise ValueError("Stream does not match the declared block length.")        
    
    return length, data


