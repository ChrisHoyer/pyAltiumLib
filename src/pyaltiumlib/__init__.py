"""
pyAltiumLib is a reader and renderer for Altium Library files
implemented in Python.
"""

__version__ = "0.1.0"

import os
from typing import Union
from pyaltiumlib.schlib.lib import SchLib
from pyaltiumlib.pcblib.lib import PcbLib

@staticmethod
def read(filepath: str) -> Union[SchLib, PcbLib]:
    """
    Read an Altium library file and return the appropriate library object.

    Args:
        filepath (str): The path to the library file.

    Returns:
        Union[SchLib, PcbLib]: The library object corresponding to the file type.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is invalid.
    """
    if not os.path.isfile( filepath ): 
        raise FileNotFoundError(f"{filepath} does not exist.")

    # Choose the correct class        
    if filepath.lower().endswith('.schlib'):
        return SchLib( filepath ) 
    
    elif filepath.lower().endswith('.pcblib'):
        return PcbLib( filepath ) 
        
    else:
        raise ValueError(f"Invalid file type: {filepath}.")
    




