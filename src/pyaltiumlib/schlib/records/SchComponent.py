from pyaltiumlib.schlib.records.base import _GenericSchRecord
from pyaltiumlib.datatypes import SchematicTextOrientation
import logging

# Set up logging
logger = logging.getLogger(__name__)

class SchComponent(_GenericSchRecord):
    """
    A class to represent a component in an Altium Schematic Library.

    Attributes:
        libreference (str): The library reference of the component.
        component_description (str): The description of the component.
        current_part_id (int): The current part ID of the component.
        part_count (int): The number of parts in the component.
        display_mode_count (int): The number of display modes.
        display_mode (int): The current display mode.
        show_hidden_pins (bool): Whether hidden pins are shown.
        library_path (str): The library path of the component.
        source_library_name (str): The source library name.
        sheet_part_file_name (str): The sheet part file name.
        target_file_name (str): The target file name.
        override_colors (bool): Whether colors are overridden.
        designator_locked (bool): Whether the designator is locked.
        part_id_locked (bool): Whether the part ID is locked.
        component_kind (int): The kind of the component.
        alias_list (str): The alias list of the component.
        orientation (SchematicTextOrientation): The orientation of the component.
    """

    def __init__(self, data, parent):
        super().__init__(data, parent)
        
        if self.record != 1:
            raise TypeError("Incorrect assigned schematic record")
                        
        self.libreference = self.rawdata.get("libreference") or self.rawdata.get("designitemid", "")
        self.component_description = self.rawdata.get("componentdescription", "")

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
        
        self.is_initialized = True
            
    def __repr__(self):
        return f"SchComponent"

    def get_bounding_box(self):
        """
        Return the bounding box for the component.

        Returns:
            None: Components do not have a bounding box.
        """
        return None

    def draw_svg(self, dwg, offset, zoom):
        """
        Draw the component using svgwrite.

        Args:
            dwg: The SVG drawing object.
            offset (CoordinatePoint): The offset for drawing.
            zoom (float): The zoom factor for scaling.
        """
        return None