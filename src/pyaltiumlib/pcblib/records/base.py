
class _GenericPCBRecord:
    
    def __init__(self, parent):
        
        self.Symbol = parent
        
        
    def read_common(self, byte_array):
        
        if len(byte_array) != 13:
            raise ValueError("Byte array length is not as expected")     
        
        self.layer = byte_array[0]
        
        self.unlocked = bool( byte_array[1] & 0x01 ) 
        self.tenting_top = bool( byte_array[1] & 0x04 ) 
        self.tenting_bottom = bool( byte_array[1] & 0x05 ) 
        self.fabrication_top = bool( byte_array[1] & 0x06 ) 
        self.fabrication_bottom = bool( byte_array[1] & 0x07 ) 
        self.keepout = bool( byte_array[2] & 0x01 )
        
        if not all(byte == 0xFF for byte in byte_array[3:13]):
            raise ValueError("Byte array spacer is not as expected")    
