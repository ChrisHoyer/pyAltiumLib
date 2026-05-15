from pyaltiumlib.base import GenericLibFile
from pyaltiumlib.datatypes import BinaryReader, ParameterCollection, PCBLayerDefinition, PCBLayerKind
from pyaltiumlib.pcblib.footprint import PcbLibFootprint

# Set up logging
import logging
logger = logging.getLogger(__name__)

class PcbLib(GenericLibFile):
    """
    PCB class for handling Altium Designer PCB library files.    
    During initialization the library file will be read.
    
    :param string filepath: The path to the .PcbLib library file   
    :param io.BytesIO oleobj: A file-like object containing the altium library file binary stream
    
    :raises FileNotFoundError: If file is not a supported file.
    :raises ValueError: If library data or header can not be read
    """
    
    def __init__(self, filepath, oleobj):
        super().__init__(filepath, oleobj)
        
        self.LibType = "PCB"
        
        self.Layers = PCBLayerDefinition.LoadDefaultLayers()
        """
        Collection with default PCB Layer Definition
        """
        
        self._ReadPCBLibrary()
        
        self.OleObj.close()
        logger.info(f"Reading and extracting of '{self.FileName}' done.")
      
 # =============================================================================
 #     Internal content reading related functions
 # =============================================================================   
     

    def _ReadPCBLibrary(self):
        try:
            self._ReadPCBFileHeader()
            self._ReadPCBLibraryData()
            self._ReadLayerKindMapping()

        except Exception as e:
            logger.error(f"Failed to read library: {e}")
            raise                   
        
    def _ReadPCBFileHeader(self):
        
        # Fileheader is different from usual string block concept
        fileheader_stream = self._OpenStream("",  "FileHeader")
        length_block = fileheader_stream.read(4)
        length_string = fileheader_stream.read(1)
        
        if int.from_bytes(length_block, "little") == int.from_bytes(length_string, "little"):
            self.LibHeader = fileheader_stream.read( int.from_bytes(length_string, "little") )
            self.LibHeader = self.LibHeader.decode("UTF-8")
            
        logger.debug(f" Fileheader of library file '{self.FileName}' is '{self.LibHeader}'.")
        if "PCB" in self.LibHeader and "Binary Library File" in self.LibHeader:
            logger.info(f"File '{self.FileName}' identified as pcb binary library file.")
        else:
            logger.warning(f"File '{self.FilePath}' can not be identified as pcb binary library!")
            
            
    def _ReadPCBLibraryData(self):

        # Parse Library Data File
        LibDataStream = self._OpenStream("Library",  "Data")
        self._FileHeader = ParameterCollection.from_block( LibDataStream )
        
        self.ComponentCount = int.from_bytes( LibDataStream.read(4), "little")
        logger.info(f"Start extracting {self.ComponentCount} component(s) from '{self.FileName}'.")
            
        for lib_ref in [BinaryReader.from_stream( LibDataStream ).read_string_block() for index in range(self.ComponentCount)]:
                self.Parts.append( PcbLibFootprint( self, lib_ref ) )


    def _ReadLayerKindMapping(self):
        try:
            stream = self.OleObj.openstream("Library/LayerKindMapping/Data")
        except Exception:
            logger.debug("No LayerKindMapping stream — skipping mechanical layer type extraction.")
            return

        raw = stream.read()
        if len(raw) < 20:
            return

        # Binary format:
        #   0: uint32  version block size (= 8)
        #   4: 8 bytes UTF-16LE version string "1.0\0"
        #  12: 4 bytes unknown
        #  16: uint32  entry count
        #  20: count * (uint32 layer_id, uint32 kind)
        version_size = int.from_bytes(raw[0:4], 'little')
        offset = 4 + version_size + 4  # skip version block + unknown bytes
        count = int.from_bytes(raw[offset:offset + 4], 'little')
        offset += 4

        MECH_BASE = 0x04000000
        layer_by_id = {layer.id: layer for layer in self.Layers}

        for _ in range(count):
            if offset + 8 > len(raw):
                break
            layer_id = int.from_bytes(raw[offset:offset + 4], 'little')
            kind     = int.from_bytes(raw[offset + 4:offset + 8], 'little')
            offset += 8

            if layer_id & 0xFF000000 == MECH_BASE:
                mech_num = layer_id & 0xFF
                if not (17 <= mech_num <= 32):
                    logger.debug(f"LayerKindMapping: unexpected extended mech number {mech_num}, skipping")
                    continue
                layer_id = 66 + mech_num  # Mechanical 17-32 → IDs 83-98

            if layer_id in layer_by_id:
                if kind in PCBLayerKind._map:
                    layer_by_id[layer_id].layer_type = PCBLayerKind(kind)
                else:
                    logger.debug(f"LayerKindMapping: unknown kind {kind:#04x} for layer {layer_id}")
            else:
                logger.debug(f"LayerKindMapping: no layer for id {layer_id}")

