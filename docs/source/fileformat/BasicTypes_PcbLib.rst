PCB Data Types
################

.. _PCBPrimitveHeader:
PCB Primitive Header
****************************
A fixed primitive header with a size of 13 :ref:`Byte` that contains layer (1 byte size) and additional flags (2 :ref:`Byte` size), followed by a spacer of 10 :ref:`Byte`.

**Example of a PCB Primitive Header:**

.. code-block:: text

    01 0C 00 FF FF FF FF FF FF FF FF FF FF

- **Layer (1 bytes):** This represents the layer used for this primitive,

- **Flag (2 byte):**  

    - bit<0>: *Unknown2*
    - bit<1>: Unlocked
    - bit<2>: *Unknown8*
    - bit<3>: *Unknown16*
    - bit<4>: TentingTop
    - bit<5>: TentingBottom
    - bit<6>: FabricationTop
    - bit<7>: FabricationBottom
    - bit<8>: KeepOut

- **Spacer (10 bytes):** `FF FF FF FF FF FF FF FF FF FF`  

.. _PCBStringBlock:
PCB String Block
****************************
A `String Block` represents a :ref:`Block` containing data structure that contains a length of the block, the length of the string and the string itself in the data. The encoding used is mostly Windows-1252 / ANSI. 

**Example of a String Block:**

.. code-block:: text

    0E 00 00 00 0D 52 45 53 20 30 32 30 31 2F 30 36 30 33

- **Block Length (4 bytes):** This represents the total block length, which `14` in decimal.

- **String Length (1 byte):** This indicates the length of the string, which is `13` in decimal.

- **Data (13 bytes):** This is the actual string data: `"RES 0201/0603"`.

.. _PCBCoordinate:
PCB Coordinate Point
****************************
A pair of (x, y)-coordinate using two :ref:`Int32`. The coordinate is stored in fixed decimal units of 1/1000 mil, e.g. 12345 = 12.345 mil.

**Example of a PCb Coordinate Point:**

.. code-block:: text

    2F 0C FE FF 00 00 00 00

- **X-Coordinate (4 bytes):** -12.7953 mil  

- **Y-Coordinate (4 bytes):** 0.0 mil  

.. _PCBPadShape:
PCB Pad Shape
****************************
Defining the shape of the Pad on the PCB using :ref:`Byte`

- 1: Round
- 2: Rectangular
- 3: Octogonal
- 9: Rounded Rectangle

.. _PCBStackMode:
PCB Stack Mode
****************************
Defining the stack mode on the PCB using :ref:`Byte`

- 1: Simple
- 2: TopMiddleBottom
- 3: FullStack

.. _PCBHoleShape:
PCB Hole Shape
****************************
Defining the hole shape of the Pad on the PCB using :ref:`Byte`

- 0: Round
- 1: Square
- 2: Slot

.. _PCBTextKind:
PCB Text Kind
****************************
 Defining the kind of the PCB text using :ref:`Int16`

- 0: Stroke
- 1: TrueType
- 2: BarCode

.. _PCBTextStrokeFont:
PCB Text Stroke Font
****************************
 Defining the stroke of the PCB text using :ref:`Byte`

- 0: Default
- 1: SansSerif
- 2: Serif

.. _PCBTextJustification:
PCB Text Justification
****************************
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