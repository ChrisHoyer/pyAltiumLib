from .mapping import _MappingBase

class PCBPadShape(_MappingBase):
    _map = {
        1: "Round",
        2: "Rectangular",
        3: "Octagonal",
        9: "Rounded Rectangle"
    }
    


    