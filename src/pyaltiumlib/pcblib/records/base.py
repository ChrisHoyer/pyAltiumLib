
class _GenericPCBRecord:
    
    def __init__(self, parent):
        
        self.Footprint = parent
        
        
    def read_common(self, byte_array):
        
        if len(byte_array) != 13:
            raise ValueError("Byte array length is not as expected")     
        
        self.layer = byte_array[0]
                
        self.unlocked = bool( byte_array[1] & 0x04 ) 
        self.tenting_top = bool( byte_array[1] & 0x20 ) 
        self.tenting_bottom = bool( byte_array[1] & 0x40 ) 
        self.fabrication_top = bool( byte_array[1] & 0x80 ) 
        self.fabrication_bottom = bool( byte_array[2] & 0x01 ) 
        self.keepout = bool( byte_array[2] & 0x02 )
        
        if not all(byte == 0xFF for byte in byte_array[3:13]):
            raise ValueError("Byte array spacer is not as expected")

        
    def get_layer_by_id(self, layerid): 
        
        for layer in self.Footprint.LibFile.Layer:
            if layer.id == layerid: 
                return layer
            
        return None

    def draw_bounding_box(self, graphic, offset, zoom):
        """
        Draws a bounding box using svgwrite.
        """
        bbox = self.get_bounding_box()
        
        start = (bbox[0] * zoom) + offset
        end = (bbox[1] * zoom) + offset
        
        size = start - end
        #start.y = start.y - size.y
        
        if size.y == 0:
            raise ValueError(f"RecordID: {self.record} - Invalid bounding box dimensions y: {bbox}")
        
        if size.x == 0:
            raise ValueError(f"RecordID: {self.record} - Invalid bounding box dimensions x: {bbox}")           
        
        graphic.add(
            graphic.rect(
                insert= start.to_int_tuple(),
                size= abs(size).to_int_tuple(),
                fill="none",
                stroke="white",
                stroke_width=1
            )
        )   