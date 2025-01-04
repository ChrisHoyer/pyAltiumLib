"""
pyAltiumLib is a reader and renderer for Altium Library files
implemented in Python.
"""

__version__ = "0.1.0"

import os

from pyaltiumlib.schlib.schlib import SchLib
from pyaltiumlib.pcblib.pcblib import PcbLib


@staticmethod
def read( filepath ):
        
    if not os.path.isfile( filepath ): 
        raise FileNotFoundError(f"{filepath} does not exist.")

    # Choose the correct class        
    if filepath.lower().endswith('.schlib'):
        return SchLib( filepath ) 
    
    elif filepath.lower().endswith('.pcblib'):
        return PcbLib( filepath ) 
        
    else:
        raise ValueError(f"Invalid file type: {filepath}.")
    




