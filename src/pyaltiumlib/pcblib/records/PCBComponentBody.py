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
        BinaryReader.from_stream( stream )

        if block.has_content():
            idx = block.data.find(b'V7_LAYER=')
            if idx >= 0:
                end = block.data.find(b'|', idx)
                if end < 0:
                    end = len(block.data)
                value = block.data[idx+9:end].decode('latin-1', errors='replace').strip()
                if value.upper().startswith('MECHANICAL'):
                    try:
                        n = int(value[10:])
                        self.layer = (56 + n) if n <= 16 else (66 + n)
                    except ValueError:
                        logger.debug(f"PcbComponentBody: could not parse layer from V7_LAYER={value}")


