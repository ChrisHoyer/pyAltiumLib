from pyaltiumlib.base import GenericLibFile
from pyaltiumlib.datatypes import BinaryReader, ParameterCollection, PCBLayerDefinition
from pyaltiumlib.pcblib.footprint import PcbLibFootprint

# Set up logging
import logging
logger = logging.getLogger(__name__)

class PcbLib(GenericLibFile):
    """
    PCB class for handling Altium Designer PCB library files.
    This class is derived from :class:`pyaltiumlib.base.GenericLibFile`.
    
    During initialization the library file will be read.
    
    :param string filepath: The path to the .PcbLib library file
    
    :raises FileNotFoundError: If file is not a supported file.
    :raises ValueError: If library data or header can not be read
    """
    
    Layers = None
    """
    Collection with default PCB Layer Definition
    """
    
    def __init__(self, filepath: str):
        """
        Initialize a PCBLib object.
        """
        super().__init__(filepath)
        
        self.LibType = "PCB"
        self.Layers = PCBLayerDefinition.LoadDefaultLayers()        
        self._ReadLibrary()
    

    def _ReadLibrary(self):
        
        self._OpenFile()
        
        self._ReadFileHeader()
        self._ReadLibraryData()

        self._CloseFile()
        
        
    def _ReadFileHeader(self):
        
        # Fileheader is different from usual string block concept
        fileheader_stream = self._OpenStream("",  "FileHeader")
        length_block = fileheader_stream.read(4)
        length_string = fileheader_stream.read(1)
        
        if int.from_bytes(length_block, "little") == int.from_bytes(length_string, "little"):
            self.LibHeader = fileheader_stream.read( int.from_bytes(length_string, "little") )
            
            
    def _ReadLibraryData(self):

        # Parse Library Data File
        LibDataStream = self._OpenStream("Library",  "Data")
        self._FileHeader = ParameterCollection.from_block( LibDataStream )
        
        self.ComponentCount = int.from_bytes( LibDataStream.read(4), "little")
            
        for lib_ref in [BinaryReader.from_stream( LibDataStream ).read_string_block() for index in range(self.ComponentCount)]:
                self.Parts.append( PcbLibFootprint( self, lib_ref ) )
            
