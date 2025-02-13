######################################
 pyAltiumLib |version| Documentation
######################################

PyAltiumLib is a tool to read Altium Designer library files. The included components are extracted. Metadata such as the description and the name of the component can be listed. It is also possible to visualize the component using the :code:`svgwrite` package. 

.. note::
   
   This documentation is build for PyAltiumLib |version|, last updated |today|.


**Quick links:** `GitHub <https://github.com/ChrisHoyer/pyAltiumLib>`__ -
`Documentation <https://pyaltiumlib.readthedocs.io/latest/>`__ -
`Python Package <https://pypi.org/project/pyaltiumlib/>`__


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