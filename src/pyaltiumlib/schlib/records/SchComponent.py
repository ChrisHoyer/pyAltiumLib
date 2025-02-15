from pyaltiumlib.schlib.records.base import GenericSchRecord
from pyaltiumlib.datatypes import SchematicTextOrientation

# Set up logging
import logging
logger = logging.getLogger(__name__)

class SchComponent(GenericSchRecord):
    """
    Implementation of a schematic record
    See also :ref:`SchPrimitive01` details on this schematic records.
    
    :param Dict data: Dictionary containing raw record data
    :param class parent: Parent symbol object
    :raises ValueError: If record id is not valid
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 1:
            logger.warning(f"Error in mapping between record objects and record id! - incorrect id {self.record}")
                        
        self.libreference = self.rawdata.get("libreference") or self.rawdata.get("designitemid", "")
        self.component_description = self.rawdata.get("componentdescription", "")

        # only if used in schematic
        self.current_part_id = int(self.rawdata.get("currentpartid", 0))
        self.part_count = int(self.rawdata.get("partcount", 1)) - 1 
        self.display_mode_count = int(self.rawdata.get("displaymodecount", 0))
        self.display_mode = int(self.rawdata.get("displaymode", 0))
        self.show_hidden_pins = self.rawdata.get_bool("showhiddenpins")

        self.library_path = self.rawdata.get("librarypath", "*")
        self.source_library_name = self.rawdata.get("sourcelibraryname", "*")
        self.sheet_part_file_name = self.rawdata.get("sheetpartfilename", "*")
        self.target_file_name = self.rawdata.get("targetfilename", "*")
        
        self.override_colors = self.rawdata.get_bool("overridecolors")
        self.designator_locked = self.rawdata.get_bool("designatorlocked")
        self.part_id_locked = self.rawdata.get_bool("partidlocked")
        self.component_kind = int(self.rawdata.get("componentkind", 0))
        
        self.alias_list = self.rawdata.get("aliaslist", "")
        self.orientation = SchematicTextOrientation(self.rawdata.get("orientation", 0))