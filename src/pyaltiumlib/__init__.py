"""
pyAltiumLib is a reader and renderer for Altium Library files
implemented in Python.
"""

AUTHOR_NAME = 'Chris Hoyer'
AUTHOR_EMAIL = 'info@chrishoyer.de'
CYEAR = '2024-2025'

__version__ = "0.6"
__author__ = "Chris Hoyer <info@chrishoyer.de>"

import os
import olefile
from typing import Union
from pyaltiumlib.schlib.lib import SchLib
from pyaltiumlib.pcblib.lib import PcbLib

# Set up logging
import logging
logger = logging.getLogger(__name__)

@staticmethod
def read(filepath: str, libfile_obj = None) -> Union[SchLib, PcbLib]:
    """
    Reads an Altium library file and returns the corresponding library object.

    This method determines whether the given file is a schematic library (`.SchLib`) 
    or a PCB library (`.PcbLib`) and returns the appropriate class instance.

    :param filepath: The path to the Altium library file.
    :type filepath: str

    :param libfile_obj: An optional binary stream (BytesIO) of the Altium library file.
                        Used when the file is read from memory instead of disk.
    :type libfile_obj: BytesIO
    
    :return: An instance of either :class:`SchLib` or :class:`PcbLib`, 
             depending on the file type.
    :rtype: :class:`pyaltiumlib.schlib.lib.SchLib` or :class:`pyaltiumlib.pcblib.lib.PcbLib`

    :raises FileNotFoundError: If the specified file does not exist.
    :raises ValueError: If the file type is not recognized as `.SchLib` or `.PcbLib`.
    """
    
    # Read from file path if no binary stream is provided
    if libfile_obj is None:
        if not os.path.isfile(filepath):
            logger.error(f"File not found: {filepath}")
            raise FileNotFoundError(f"File not found: {filepath}")
        
        if not olefile.isOleFile(filepath):
            logger.error(f"Unsupported file format: {filepath}")
            raise ValueError(f"Unsupported file format: {filepath}")

        libfile_ole = olefile.OleFileIO(filepath)

    # Read from an in-memory BytesIO object
    else:
        if not olefile.isOleFile(libfile_obj):
            logger.error(f"Unsupported file format in memory for: {filepath}")
            raise ValueError(f"Unsupported file format in memory for: {filepath}")

        libfile_ole = olefile.OleFileIO(libfile_obj)

    # Determine file type and return the appropriate library object
    if filepath.lower().endswith('.schlib'):
        return SchLib(filepath, libfile_ole)
    
    if filepath.lower().endswith('.pcblib'):
        return PcbLib(filepath, libfile_ole)

    logger.error(f"Invalid file type: {filepath}")
