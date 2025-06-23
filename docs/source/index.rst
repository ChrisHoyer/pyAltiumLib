######################################
 pyAltiumLib |version| Documentation
######################################

PyAltiumLib is a tool to read Altium Designer library files. The included components are extracted. Metadata such as the description and the name of the component can be listed. It is also possible to visualize the component using the :code:`svgwrite` package. 

.. note::
   
   This documentation is build for PyAltiumLib |version|, last updated |today|.


**Quick links:** `GitHub <https://github.com/ChrisHoyer/pyAltiumLib>`__ -
`Documentation <https://pyaltiumlib.readthedocs.io/latest/>`__ -
`Python Package <https://pypi.org/project/pyaltiumlib/>`__


This tool is created based on the details given in several open-source repositories:

- `Altium-Schematic-Parser <https://github.com/a3ng7n/Altium-Schematic-Parser>`_
- `Altium Library Parsing <https://github.com/fierst/AltiumLibParser>`_
- `Altium schematic file format <https://github.com/vadmium/python-altium/blob/master/format.md>`_
- `AltiumParser <https://github.com/bugadani/AltiumParser>`_
- `python-altium <https://github.com/matthiasbock/python-altium>`_
- `AltiumSharp <https://github.com/issus/AltiumSharp>`_

.. toctree::
   :caption: Introduction
   :maxdepth: 1

   usage/install
   usage/release
   
.. toctree::
   :caption: API Reference
   :maxdepth: 1

   classes/LibFile
   classes/Components
   classes/Datatypes
   classes/Records

.. toctree::
   :caption: Altium File Format
   :maxdepth: 1

   fileformat/FileStructure
   fileformat/BasicTypes
   fileformat/Primitives