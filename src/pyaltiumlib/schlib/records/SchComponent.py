"""
Schematic Pin Record


"""

from pyaltiumlib.schlib.records.base import _SchCommonParam
from pyaltiumlib.datatypes import SchematicTextOrientation


class SchComponent(_SchCommonParam):
    
    def __init__(self, data):
        
        super().__init__(data)
        
        if not( self.record == 1 ):
            raise TypeError("Incorrect assigned schematic record")
                        
        self.libreference = self.rawdata.get("libreference") or self.rawdata.get("designitemid", "")
        self.component_description = self.rawdata.get("componentdescription", "")

        self.current_part_id = int(self.rawdata.get("currentpartid", 0))
        
        # Adjust part count
        self.part_count = int(self.rawdata.get("partcount", 1)) - 1 
        
        self.display_mode_count = int(self.rawdata.get("displaymodecount", 0))
        self.display_mode = int(self.rawdata.get("displaymode", 0))
        self.show_hidden_pins = self.rawdata.get("showhiddenpins", "F").upper() == "T"

        self.library_path = self.rawdata.get("librarypath", "*")
        self.source_library_name = self.rawdata.get("sourcelibraryname", "*")
        self.sheet_part_file_name = self.rawdata.get("sheetpartfilename", "*")
        self.target_file_name = self.rawdata.get("targetfilename", "*")
        
        self.override_colors = self.rawdata.get("overridecolors", "F").upper() == "T"
        self.designator_locked = self.rawdata.get("designatorlocked", "F").upper() == "T"
        self.part_id_locked = self.rawdata.get("partidlocked", "F").upper() == "T"
        self.component_kind = int(self.rawdata.get("componentkind", 0))
        
        self.alias_list = self.rawdata.get("aliaslist", "")
        self.orientation = SchematicTextOrientation( self.rawdata.get("orientation", 0))
            
        
    def __repr__(self):
        return f"SchComponent "        
        

        
    



