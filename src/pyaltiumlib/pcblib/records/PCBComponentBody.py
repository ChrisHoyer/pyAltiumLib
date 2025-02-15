from pyaltiumlib.pcblib.records.base import GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader


# Configure logging
import logging
logger = logging.getLogger(__name__)

class PcbComponentBody(GenericPCBRecord):
    """
    Implementation of a pcb record
    See also :ref:`PCBPrimitive12` details on this PCB records. This record can be drawn.
    
    :param class parent: Parent symbol object 
    :param Dict data: Dictionary containing raw record data
    """    
    def __init__(self, parent, stream):
        
        super().__init__(parent)
                
        block = BinaryReader.from_stream( stream )
        string = BinaryReader.from_stream( stream )
        
        
