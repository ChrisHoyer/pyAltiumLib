Contributing and Coverage 
**************************

Contributing to pyAltiumLib
===========================

This is a personal open source project that has been developed in my spare time. Any kind of contribution, suggestion, feedback or bug report is very welcome.

If you want to suggest improvements, report a bug or any other problem, please use the `issue report page and provide <https://github.com/ChrisHoyer/pyAltiumLib/issues>`__ all the information and files needed to reproduce the problem.

The code is available in `this repository <https://github.com/ChrisHoyer/pyAltiumLib>`__ on GitHub. Feel free, to submit improvements or bug fixes using forks and pull requests.


File Format Coverage
=======================

Currently, the format is not completely supported, some aspects are not fully implemented. Not all containers or records are known yet, so this list and the associated documentation may be incomplete.

The coverage of containers of the Altium library file format is shown below:

.. list-table:: Schematic Library Container Coverage
   :header-rows: 1

   * - Library
     - File
     - Coverage
   * - Schematic Library
     - FileHeader
     - Key features are implemented
   * - Schematic Library
     - Data
     - Key features are implemented
   * - Schematic Library
     - Storage
     - Not implemented
   * - Schematic Library
     - <symbol>/PinFrac
     - Not implemented
   * - Schematic Library
     - <symbol>/PinSymbolLineWidth
     - Not implemented
   * - Schematic Library
     - <symbol>/PinWideText
     - Not implemented
   * - Schematic Library
     - <symbol>/PinTextData
     - Not implemented
   * - Schematic Library
     - <symbol>/PinFunctionData
     - Not implemented

.. list-table:: PCB Library Container Coverage
   :header-rows: 1

   * - Library
     - File
     - Coverage
   * - PCB Library
     - FileHeader
     - Key features are implemented
   * - PCB Library
     - FileVersionInfo/Header
     - Not implemented
   * - PCB Library
     - FileVersionInfo/Data
     - Not implemented
   * - PCB Library
     - Library/ComponentParamsTOC/Data
     - Not implemented
   * - PCB Library
     - Library/ComponentParamsTOC/Header
     - Not implemented
   * - PCB Library
     - Library/LayerKindMapping/Header
     - Not implemented
   * - PCB Library
     - Library/LayerKindMapping/Data
     - Not implemented
   * - PCB Library
     - Library/Models/Header
     - Not implemented
   * - PCB Library
     - Library/Models/Data
     - Not implemented
   * - PCB Library
     - Library/Models/<Embedded 3D Model>
     - Not implemented
   * - PCB Library
     - Library/ModelsNoEmbed/Header
     - Not implemented
   * - PCB Library
     - Library/ModelsNoEmbed/Data
     - Not implemented
   * - PCB Library
     - Library/PadViaLibrary/Header
     - Not implemented
   * - PCB Library
     - Library/PadViaLibrary/Data
     - Not implemented
   * - PCB Library
     - Library/Textures/Header
     - Not implemented
   * - PCB Library
     - Library/Textures/Data
     - Not implemented
   * - PCB Library
     - Library/Header
     - Not implemented
   * - PCB Library
     - Library/Data
     - Key features are implemented
   * - PCB Library
     - Library/EmbeddedFonts
     - Not implemented
   * - PCB Library
     - <footprint>/PrimitiveGuids/Header
     - Not implemented
   * - PCB Library
     - <footprint>/PrimitiveGuids/Data
     - Not implemented
   * - PCB Library
     - <footprint>/UniqueIDPrimitiveInformation/Header
     - Not implemented
   * - PCB Library
     - <footprint>/UniqueIDPrimitiveInformation/Data
     - Not implemented
   * - PCB Library
     - <footprint>/Header
     - Not implemented
   * - PCB Library
     - <footprint>/Data
     - Key features are implemented
   * - PCB Library
     - <footprint>/Parameters
     - Not implemented
   * - PCB Library
     - <footprint>/WideStrings
     - Not implemented


The coverage of records/primitives of the Altium library file format is shown below:

.. list-table:: Schematic Library Record Coverage
   :header-rows: 1

   * - Library
     - Record
     - Coverage
   * - Schematic Record
     - Component
     - Key features implemented
   * - Schematic Record
     - Pin
     - Implemented
   * - Schematic Record
     - IEEE Symbol
     - Not Implemented
   * - Schematic Record
     - Label
     - Implemented
   * - Schematic Record
     - Bezier
     - Implemented
   * - Schematic Record
     - Polyline
     - Implemented
   * - Schematic Record
     - Polygon
     - Implemented
   * - Schematic Record
     - Ellipse
     - Implemented
   * - Schematic Record
     - Pie
     - Not Implemented
   * - Schematic Record
     - Round Rectangle
     - Implemented
   * - Schematic Record
     - Elliptical Arc
     - Implemented
   * - Schematic Record
     - Arc
     - Implemented
   * - Schematic Record
     - Line
     - Implemented
   * - Schematic Record
     - Rectangle
     - Implemented
   * - Schematic Record
     - Images
     - Not Implemented
   * - Schematic Record
     - Designator
     - Implemented
   * - Schematic Record
     - Parameter
     - Implemented

.. list-table:: PCB Library Record Coverage
   :header-rows: 1

   * - Library
     - Record
     - Coverage
   * - PCB Primitives
     - Arc
     - Key features implemented
   * - PCB Primitives
     - Pad
     - Key features implemented
   * - PCB Primitives
     - Via
     - Key features implemented
   * - PCB Primitives
     - Track
     - Implemented
   * - PCB Primitives
     - String
     - Implemented
   * - PCB Primitives
     - Fill
     - Implemented
   * - PCB Primitives
     - Region
     - Implemented
   * - PCB Primitives
     - Component Body
     - Not Implemented


Open points
=======================

- Schematic symbols with more than one part can be read and drawn. However, all sub parts are rendered above each other. To seperate each sub part, the owner index must be considered.