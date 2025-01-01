:topic: Data types Schematic

Schematic Data Types
#####################

.. _SchCommonParameter:
Schematic Common Parameter
****************************

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

.. _SchCoordinate:
Schematic Coordinate Point
****************************
 A singular coordinate based on two parameter for each tuple from a :ref:`ParameterCollection`. The parameters from this tuple are :code:`num`, which represents the number, and :code:`frac` represents the fraction. If one of the tuples is not given, the value is zero. Each of this tuples is calucated to a decimal value using :code:`num * 10.0 + frac / 10000.0`

**Example of a Schematic Coordinate:**

.. code-block:: text

    Radius=10|Radius_FRAC=500

- **Coordinate:** 100.05 mil  



.. _SchCoordinatePoint:
Schematic Coordinate Point
****************************
 A pair of (x, y)-coordinate :ref:`SchCoordinate` based on two parameter for each tuple from a :ref:`ParameterCollection`. The parameters from this tuple are :code:`num`, which represents the number, and :code:`frac` represents the fraction. If one of the tuples is not given, the value is zero. Each of this tuples is calucated to a decimal value using :code:`num * 10.0 + frac / 10000.0`

**Example of a Schematic Coordinate Point:**

.. code-block:: text

    LOCATION.X=10|LOCATION.X_FRAC=500|LOCATION.Y=200

- **X-Coordinate:** 100.05 mil  

- **Y-Coordinate:** 2000.0 mil  

.. _SchLineWidth:
Schematic Line Width
****************************
 Defining the line width of schematic elements

- 0: Smallest
- 1: Small
- 2: Medium
- 3: Large

.. _SchLineStyle:
Schematic Line Style
****************************
 Defining the line style of schematic elements

- 0: Solid
- 1: Dashed
- 2: Dotted
- 3: Large

.. _SchLineShape:
Schematic Line Shape
****************************
 Defining the line shape of schematic elements

- 0: None
- 1: Arrow
- 2: Solid Arrow
- 3: Tail
- 4: Solid Tail
- 5: Circle
- 6: Square

.. _SchPinFlags:
Schematic Pin Flags
****************************
 Flags defining some properties of the schematic pin using :ref:`Byte`

- bit<0>: None
- bit<1>: Rotated
- bit<2>: Flipped
- bit<3>: Hide
- bit<4>: Display Name Visible
- bit<5>: Desginator Visible
- bit<6>: *unknown*
- bit<7>: Graphically Locked

.. _SchPinElectricalType:
Schematic Pin Electrical Type
*******************************
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
**************************
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
****************************
 Defining the orientation of a schematic text

- 0: None
- 1: Rotated
- 2: Flipped

.. _SchTextJustification:
Schematic Text Justification
****************************
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