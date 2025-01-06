###################
Altium File Format
###################

This documentation provides an overview of the structure, data organization and components of the Altium file formats `.pcblib` (PCB library) and `.schlib` (schematic library). This guide combines information from several open-source repositories:

- `Altium-Schematic-Parser <https://github.com/a3ng7n/Altium-Schematic-Parser>`_
- `Altium Library Parsing <https://github.com/fierst/AltiumLibParser>`_
- `Altium schematic file format <https://github.com/vadmium/python-altium/blob/master/format.md>`_
- `AltiumParser <https://github.com/bugadani/AltiumParser>`_
- `python-altium <https://github.com/matthiasbock/python-altium>`_
- `AltiumSharp <https://github.com/issus/AltiumSharp>`_


These resources provide insights into the format used, which is essential for developing tools. The file formats are based on the Microsoft OLE (Object Linking and Embedding) standard, which organizes data (streams) into hierarchical containers.

.. toctree::
   :maxdepth: 4
   :titlesonly:

   BasicTypes
   Primitives
   PCBLib
   SchLib