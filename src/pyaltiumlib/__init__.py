"""
pyAltiumLib is a reader and renderer for Altium Library files
implemented in Python.
"""

AUTHOR_NAME = 'Chris Hoyer'
AUTHOR_EMAIL = 'info@chrishoyer.de'
CYEAR = '2024-2025'

__version__ = "0.4"
__author__ = "Chris Hoyer <info@chrishoyer.de>"

import os
from typing import Union
from pyaltiumlib.schlib.lib import SchLib
from pyaltiumlib.pcblib.lib import PcbLib

# Set up logging
import logging
logger = logging.getLogger(__name__)

@staticmethod
def read(filepath: str) -> Union[SchLib, PcbLib]:
    """
    Reads an Altium library file and returns the corresponding library object.

    This method determines whether the given file is a schematic library (`.SchLib`) 
    or a PCB library (`.PcbLib`) and returns the appropriate class instance.

    :param filepath: The path to the Altium library file.
    :type filepath: str

    :return: An instance of either :class:`SchLib` or :class:`PcbLib`, 
             depending on the file type.
    :rtype: :class:`pyaltiumlib.schlib.lib.SchLib` or :class:`pyaltiumlib.pcblib.lib.PcbLib`

    :raises FileNotFoundError: If the specified file does not exist.
    :raises ValueError: If the file type is not recognized as `.SchLib` or `.PcbLib`.
    """
    if not os.path.isfile( filepath ): 
        logger.error(f"{filepath} does not exist.")
        raise

    # Choose the correct class        
    if filepath.lower().endswith('.schlib'):
        return SchLib( filepath ) 
    
    elif filepath.lower().endswith('.pcblib'):
        return PcbLib( filepath ) 
        
    else:
        logger.error(f"Invalid file type: {filepath}.")
        raise
