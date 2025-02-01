Data Types
***************

Common Data Types
==================

.. _Block:

Block
-----
A `Block` represents a data structure that contains the length of the block and the data of the block itself. The data can be in different formats, e.g. string or byte or a composite. The first 4 bytes are little-endian and define the length of the block.

.. _ParameterCollection:

Parameter Collection
-----------------------
A `Parameter Collection` represents a :ref:`Block` containing separated parameters as data, each 0x00 terminated. The encoding used is mostly Windows-1252 / ANSI.

Each parameter in the collection is separated using :code:`|`. The key and value of each parameter are separated by an :code:`=` symbol.


**Example of a Parameter Collection:**

.. code-block:: text
    
    48 00 00 00 7C 46 49 4C 45 4E 41 4D 45 3D 43 3A
    5C 4C 69 62 72 61 72 79 5C 44 65 73 69 67 6E 5C
    52 65 73 69 73 74 6F 72 73 2E 24 24 24 7C 44 41
    54 45 3D 30 39 2E 31 32 2E 32 30 32 34 7C 54 49
    4D 45 3D 31 30 3A 34 34 3A 32 34 00

- **Block Length (4 bytes):** This represents the total block length, which `72` in decimal. 

- **Data (72 bytes):**

.. code-block:: text
    
    |FILENAME=C:\Library\Design\Resistors.$$$|DATE=09.12.2024|TIME=10:44:24

.. _Color:

Color
-------
Color as defined in GDI+ structures.



.. _UInt32:

Unsigned Integer (32-bit)
-------------------------
Represents a 32-bit unsigned integer.

**Schematic Record:** Default value if property is missing seems to be :code:`0`.

.. _Int32:

Signed Integer (32-bit)
-------------------------
Represents a 32-bit signed integer.

**Schematic Record:** Default value if property is missing seems to be :code:`0`.

.. _Int16:

Signed Integer (16-bit)
-------------------------
Represents a 16-bit signed integer.

**Schematic Record:** Default value if property is missing seems to be :code:`0`.

.. _Double:

Double
-------------------------
Represents a 64-bit floating-point number. Typically three decimal places.

**Schematic Record:** property omitted if property is missing.

.. _Boolean:

Boolean
-------------------------
Represents a boolean value (True or False).

**Schematic Record:** Either :code:`T` for true or :code:`F` for false. When false, the property is often omitted, rather than explicitly set to false.

.. _Byte:

Byte
-------------------------
Represents a single byte (8 bits).

.. _String:

String
-------------------------
Represents a ASCII string.

PCB Data Types
==================

.. _PCBPrimitveHeader:

PCB Primitive Header
-----------------------
A fixed primitive header with a size of 13 :ref:`Byte` that contains layer (1 byte size) and additional flags (2 :ref:`Byte` size), followed by a spacer of 10 :ref:`Byte`.

**Example of a PCB Primitive Header:**

.. code-block:: text

    01 0C 00 FF FF FF FF FF FF FF FF FF FF

- **Layer (1 bytes):** This represents the layer used for this primitive,

- **Flag (2 byte):**  

    - bit<0>: *Unknown2*
    - bit<1>: *Unknown2*
    - bit<2>: Unlocked
    - bit<3>: *Unknown8*
    - bit<4>: *Unknown16*
    - bit<5>: TentingTop
    - bit<6>: TentingBottom
    - bit<7>: FabricationTop
    - bit<8>: FabricationBottom
    - bit<9>: KeepOut

- **Spacer (10 bytes):** `FF FF FF FF FF FF FF FF FF FF`  

.. _PCBStringBlock:

PCB String Block
-----------------------
A `String Block` represents a :ref:`Block` containing data structure that contains a length of the block, the length of the string and the string itself in the data. The encoding used is mostly Windows-1252 / ANSI. 

**Example of a String Block:**

.. code-block:: text

    0E 00 00 00 0D 52 45 53 20 30 32 30 31 2F 30 36 30 33

- **Block Length (4 bytes):** This represents the total block length, which `14` in decimal.

- **String Length (1 byte):** This indicates the length of the string, which is `13` in decimal.

- **Data (13 bytes):** This is the actual string data: `"RES 0201/0603"`.

.. _PCBCoordinate:

PCB Coordinate Point
-----------------------
A pair of (x, y)-coordinate using two :ref:`Int32`. The coordinate is stored in fixed decimal units of 1/1000 mil, e.g. 12345 = 12.345 mil.

**Example of a PCb Coordinate Point:**

.. code-block:: text

    2F 0C FE FF 00 00 00 00

- **X-Coordinate (4 bytes):** -12.7953 mil  

- **Y-Coordinate (4 bytes):** 0.0 mil  

.. _PCBPadShape:

PCB Pad Shape
-----------------------
Defining the shape of the Pad on the PCB using :ref:`Byte`

- 1: Round
- 2: Rectangular
- 3: Octogonal
- 9: Rounded Rectangle

.. _PCBStackMode:

PCB Stack Mode
-----------------------
Defining the stack mode on the PCB using :ref:`Byte`

- 1: Simple
- 2: TopMiddleBottom
- 3: FullStack

.. _PCBHoleShape:

PCB Hole Shape
-----------------------
Defining the hole shape of the Pad on the PCB using :ref:`Byte`

- 0: Round
- 1: Square
- 2: Slot

.. _PCBTextKind:

PCB Text Kind
-----------------------
 Defining the kind of the PCB text using :ref:`Int16`

- 0: Stroke
- 1: TrueType
- 2: BarCode

.. _PCBTextStrokeFont:

PCB Text Stroke Font
-----------------------
 Defining the stroke of the PCB text using :ref:`Byte`

- 0: Default
- 1: SansSerif
- 2: Serif

.. _PCBTextJustification:

PCB Text Justification
-----------------------
 Defining the justification of the PCB text using :ref:`Byte`

- 1: BottomRight
- 2: MiddleRight
- 3: TopRight
- 4: BottomCenter
- 5: MiddleCenter
- 6: TopCenter
- 7: BottomLeft
- 8: MiddleLeft
- 9: TopLeft

:topic: Data types Schematic

Schematic Data Types
=====================

.. _SchRecord:

Schematic Record
-----------------------

A `Schematic Record` represents a strcture similar to :ref:`Block`. The length is given by the first 2 bytes and the record type is given by the next 2 bytes. There are two different record types identified

- :code:`0x01` as ASCII type, which can be read using :ref:`ParameterCollection`
- :code:`0x02` as binary Type

The binary type is so far only used for schematic pins and is described in :ref:`SchBinaryPin`

.. _SchCommonParameter:

Schematic Common Parameter
---------------------------

 Each record has the following set as default parameters in the :ref:`ParameterCollection`:

.. list-table::
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Description**
   * - Record
     - :ref:`Int32`
     - 
   * - IsNotAccessible
     - :ref:`Boolean`
     - 
   * - OwnerIndex
     - :ref:`Int32`
     - 
   * - OwnerPartId
     - :ref:`Boolean`
     - Link to object's parent ID
   * - OwnerPartDisplayMode
     - :ref:`Int32`
     - Graphical representation of schematic components
   * - GraphicallyLocked
     - :ref:`Boolean`
     - 
   * - UniqueID
     - :ref:`Int32`
     - 

For graphical records, there are additional parameters:

.. list-table::
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Description**
   * - Location
     - :ref:`SchCoordinate`
     - X/Y Coordinate
   * - Color
     - :ref:`Color`
     - Edge Color
   * - AreaColor
     - :ref:`Color`
     - Fill Color


.. _SchBinaryPin:

Schematic Binary Pin
-----------------------
Schematic binary pin record (record type :code:`0x02`):

.. list-table:: 
   :header-rows: 1

   * - Parameter
     - Size (Bytes)
     - Datatype
     - Description
   * - Record
     - 4
     - :ref:`UInt32`
     - Record ID
   * - *unknown*
     - 1
     - :ref:`Byte`
     - 
   * - OwnerPartId
     - 1
     - :ref:`Byte`
     - 
   * - OwnerPartDisplayMode
     - 1
     - :ref:`Byte`
     - 
   * - Symbol_InnerEdge
     - 1
     - :ref:`Byte`
     - 
   * - Symbol_OuterEdge
     - 1
     - :ref:`Byte`
     - 
   * - Symbol_Inside
     - 1
     - :ref:`Byte`
     - 
   * - Symbol_Outside
     - 1
     - :ref:`Byte`
     - 
   * - Symbol_Linewidth
     - 
     - 
     - Not implemented?
   * - Description Length
     - 1
     - :ref:`Byte`
     - 
   * - Description
     - Variable
     - :ref:`String`
     - 
   * - Electrical_Type
     - 1
     - :ref:`Byte`
     - 
   * - Rotated
     - 1 (Bit 0)
     - :ref:`Boolean`
     - 
   * - Flipped
     - 1 (Bit 1)
     - :ref:`Boolean`
     - 
   * - Hide
     - 1 (Bit 2)
     - :ref:`Boolean`
     - 
   * - Show_Name
     - 1 (Bit 3)
     - :ref:`Boolean`
     - 
   * - Show_Designator
     - 1 (Bit 4)
     - :ref:`Boolean`
     - 
   * - Graphically_Locked
     - 1 (Bit 6)
     - :ref:`Boolean`
     - 
   * - Length
     - 2
     - :ref:`Int16`
     - 
   * - Location
     - 4
     - :ref:`SchCoordinate`
     - 
   * - Color
     - 4
     - :ref:`Color`
     - 
   * - Name Length
     - 1
     - :ref:`Byte`
     - 
   * - Name
     - Variable
     - :ref:`String`
     - 
   * - Designator Length
     - 1
     - :ref:`Byte`
     - 
   * - Designator
     - Variable
     - :ref:`String`
     - 


.. _SchCoordinate:

Schematic Coordinate Point
---------------------------
 A singular coordinate based on two parameter for each tuple from a :ref:`ParameterCollection`. The parameters from this tuple are :code:`num`, which represents the number, and :code:`frac` represents the fraction. If one of the tuples is not given, the value is zero. Each of this tuples is calucated to a decimal value using :code:`num + frac / 1000.0`

**Example of a Schematic Coordinate:**

.. code-block:: text

    Radius=10|Radius_FRAC=500

- **Coordinate:** 100.05 mil  

.. _SchCoordinatePoint:

Schematic Coordinate Point
---------------------------
 A pair of (x, y)-coordinate :ref:`SchCoordinate` based on two parameter for each tuple from a :ref:`ParameterCollection`. The parameters from this tuple are :code:`num`, which represents the number, and :code:`frac` represents the fraction. If one of the tuples is not given, the value is zero. Each of this tuples is calucated to a decimal value using :code:`num + frac / 1000.0`

**Example of a Schematic Coordinate Point:**

.. code-block:: text

    LOCATION.X=10|LOCATION.X_FRAC=500|LOCATION.Y=200

- **X-Coordinate:** 100.05 mil  

- **Y-Coordinate:** 2000.0 mil  

.. _SchLineWidth:

Schematic Line Width
---------------------------
 Defining the line width of schematic elements.

- 0: Smallest
- 1: Small
- 2: Medium
- 3: Large

.. _SchLineStyle:

Schematic Line Style
---------------------------
 Defining the line style of schematic elements. This parameter is given by a :ref:`ParameterCollection` using the key :code:`linestyle` or :code:`linestyleext`.

- 0: Solid (default)
- 1: Dashed
- 2: Dotted
- 3: Dash Dotted

.. _SchLineShape:

Schematic Line Shape
---------------------------
 Defining the line shape of schematic elements. This parameter is given by a :ref:`ParameterCollection` using the key :code:`endlineshape` or :code:`startlineshape`.

- 0: None (default)
- 1: Arrow
- 2: Solid Arrow
- 3: Tail
- 4: Solid Tail
- 5: Circle
- 6: Square

.. _SchPinFlags:

Schematic Pin Flags
---------------------------
 Flags defining some properties of the schematic pin using :ref:`Byte`

- bit<0>: Rotated
- bit<1>: Flipped
- bit<2>: Hide
- bit<3>: Display Name Visible
- bit<4>: Desginator Visible
- bit<5>: *unknown*
- bit<6>: Graphically Locked

.. _SchPinElectricalType:

Schematic Pin Electrical Type
------------------------------
 Defining the electrical type of the schematic pin

- 0: Input
- 1: Input/Output
- 2: Output
- 3: Open Collector
- 4: Passive
- 5: High Impedanz (HiZ)
- 6: Open Emitter
- 7: Power

.. _SchPinSymbol:

Schematic Pin Symbol
---------------------------
 Defining the symbol of the schematic pin

- 0: None
- 1: Dot
- 2: Right Left Signal Flow
- 3: Clock
- 4: Active Low Input
- 5: Analog Signal Input
- 6: Not Logic Connection
- 8: Postponed Output
- 9: Open Collector
- 10: High Impednaz (HiZ)
- 11: High Current
- 12: Pulse
- 13: Schmitt
- 17: Active Low Output
- 22: Open Collector Pull up
- 23: Open Emitter
- 24: Open Emitter Pull up
- 25: Digital Signal Input
- 30: Shift Left
- 32: Open Outout
- 33: Left Right Signal Flow
- 34: Bidirectional Signal Flow

.. _SchTextOrientation:

Schematic Text Orientation
---------------------------
 Defining the orientation of a schematic text. This parameter is given by a :ref:`ParameterCollection` using the key :code:`Orientation`.

- 0: None
- 1: Rotated 90 degrees
- 2: Rotated 180 degrees (Flipped)
- 3: Rotated 270 degrees (Flipped)

.. _SchTextJustification:

Schematic Text Justification
-----------------------------
 Defining the orientation of a schematic text

- 0: BottomLeft
- 1: BottomCenter
- 2: BottomRight
- 3: MiddleLeft
- 4: MiddleCenter
- 5: MiddleRight
- 6: TopLeft
- 7: TopCenter
- 8: TopRight