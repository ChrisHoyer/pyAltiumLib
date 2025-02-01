PCB Library (.pcblib)
************************

The `.pcblib` file format stores PCB footprints. It is based on OLE (Object Linking and Embedding) format, a compound document standard from Microsoft. 

The format follows a structured hierarchy, with several storage containers and data blocks. Below is an overview of the typical structure:

::

   <file.pcblib>/
   ├── FileHeader
   ├── FileVersionInfo/
   │   ├── Header
   │   └── Data
   ├── Library/
   │   ├── ComponentParamsTOC/
   │   │   ├── Header
   │   │   └── Data
   │   ├── LayerKindMapping/
   │   │   ├── Header
   │   │   └── Data
   │   ├── Models/
   │   │   ├── Header
   │   │   ├── Data
   │   │   ├── <Embedded 3D Model>
   │   │   └── ...
   │   ├── ModelsNoEmbed/
   │   │   ├── Header
   │   │   └── Data
   │   ├── PadViaLibrary/
   │   │   ├── Header
   │   │   └── Data
   │   ├── Textures/
   │   │   ├── Header
   │   │   └── Data
   │   ├── Header
   │   ├── Data
   │   └── EmbeddedFonts
   ├── <footprint>/
   │   ├── PrimitiveGuids/
   │   │   ├── Header
   │   │   └── Data
   │   ├── UniqueIDPrimitiveInformation/
   │   │   ├── Header
   │   │   └── Data
   │   ├── Header
   │   ├── Data
   │   ├── Parameters
   │   └── WideStrings
   └── ...

This list is incomplete and is limited to the essentials for reading and displaying footprints.

Container Library
=====================

Contains common elements used in the library as well as a table of contents (TOC)

- Structure of :code:`Library/Header`:
   #. Number of datasets as :ref:`UInt32`

- Structure of :code:`Library/Data`:
   #. Library header as :ref:`ParameterCollection`
   #. Number of footprints as :ref:`UInt32`
   #. Each footprint name as :ref:`PCBStringBlock`

Container Library/ComponentParamsTOC
=====================================

Contains name, description, height and pad count of each footprint.

- Structure of :code:`Library/ComponentParamsTOC/Header`:
   #. Number of datasets as :ref:`UInt32`

- Structure of :code:`Library/ComponentParamsTOC/Data`:
   #. Parameter of each component as :ref:`ParameterCollection`

Container Library/Models
========================

Contains embedded 3D models, if used in the footprint.

- Structure of :code:`Library/Models/Header`:
   #. Number of embedded models as :ref:`UInt32`

- Structure of :code:`Library/Models/Data`:
   #. Parameter of each embedded model as :ref:`ParameterCollection`

- Structure of :code:`Library/Models/<Embedded 3D Model>`:
   #. Embedded Models are stored as ASCII STEP files but using zlib compression

Container <footprint>
======================

A container for each individual footprint. Each footprint consists of multiple primitives. A primitive is a single drawing element, such as a line, arc, rectangle, or pad. The naming of this container has some limitations due to the compound document standard. The maximum text length is 31, container names longer than 31 will be truncated. Also, if a :code:`/` is used in the name, it will be replaced by a :code:`_`.

- Structure of :code:`<footprint>/Header`:
   #. Number of primitives used in the footprint as :ref:`UInt32`

- Structure of :code:`<footprint>/Data`:
   #. Footprint name as :ref:`PCBStringBlock`
   #. List of Primitives

      #. PrimitiveID as :ref:`UInt32`.
      #. Primitive as :ref:`PCBPrimitives`

- Structure of :code:`<footprint>/WideStrings`:
   #. List of encoded text as :ref:`ParameterCollection`

       - Each string entry is encoded inside a parameter string value with a comma separated list of integers.
       - Those values are interpreted as UTF-16 code-points.

- Structure of :code:`<footprint>/Parameters`:
   #. List of parameters as :ref:`ParameterCollection`
   #. Default parameters:

       - PATTERN
       - HEIGHT
       - DESCRIPTION
       - ITEMGUID
       - REVISIONGUID