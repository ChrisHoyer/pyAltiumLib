File Structure
***************

This documentation provides an overview of the structure, data organization and components of the Altium file formats `.pcblib` (PCB library) and `.schlib` (schematic library). This guide combines information from several open-source repositories:

- `Altium-Schematic-Parser <https://github.com/a3ng7n/Altium-Schematic-Parser>`_
- `Altium Library Parsing <https://github.com/fierst/AltiumLibParser>`_
- `Altium schematic file format <https://github.com/vadmium/python-altium/blob/master/format.md>`_
- `AltiumParser <https://github.com/bugadani/AltiumParser>`_
- `python-altium <https://github.com/matthiasbock/python-altium>`_
- `AltiumSharp <https://github.com/issus/AltiumSharp>`_


These resources provide insights into the format used, which is essential for developing tools. The file formats are based on the Microsoft OLE (Object Linking and Embedding) standard, which organizes data (streams) into hierarchical containers.

**File Structure**

.. raw:: html
    :file: ./LibraryFile_Container.drawio.html

The basic structure is organized in containers. Each library file contains several subcontainers with the component as a footprint or symbol. Each component is composed of so-called records. These records contain the visible structures such as rectangles, polygons and lines. The records for footprints are binary data. Schematic records are mostly parameter collections.
