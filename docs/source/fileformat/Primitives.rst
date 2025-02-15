Primitives and Records
***********************

.. _PCBPrimitives:

PCB Primitives
=====================

.. _PCBPrimitive01:

ID 1 - Arc
-------------------

Represents a footprint arc primitive. Contains only one :ref:`Block` with the following data:

.. list-table:: 
   :header-rows: 1
   :widths: auto

   * - **Name**
     - **Size (Bytes)**
     - **Datatype**
     - **Comment**
   * - Primitive Header
     - 13
     - :ref:`PCBPrimitveHeader`
     - 
   * - Location
     - 8
     - :ref:`PCBCoordinate`
     - 
   * - Radius
     - 4
     - :ref:`Int32`
     - 
   * - StartAngle
     - 8
     - :ref:`Double`
     - 
   * - EndAngle
     - 8
     - :ref:`Double`
     - 
   * - Width
     - 4
     - :ref:`Int32`
     - 
   * - *Unknown*
     - 4
     - :ref:`Int32`
     - Only of length >= 56
   * - *Unknown*
     - 2
     - :ref:`Int16`
     - Only of length >= 56
   * - *Unknown*
     - 1
     - :ref:`Byte`
     - Only of length >= 56
   * - *Unknown*
     - 4
     - :ref:`Int32`
     - Only of length >= 56


.. _PCBPrimitive02:

ID 2 - Pad
-------------------

Represents a footprint pad primitive. Structured as:

#. Designator as :ref:`PCBStringBlock`
#. *Unknown* as :ref:`Block`
#. *Unknown* constant :code:`|&|0` as :ref:`PCBStringBlock`
#. *Unknown* as :ref:`Block`
#. First :ref:`Block` on information
#. Second :ref:`Block` on information

First block on information:

.. list-table:: 
   :header-rows: 1
   :widths: auto

   * - **Name**
     - **Size (Byte)**
     - **Datatype**
     - **Comment**
   * - Primitive Header
     - 13
     - :ref:`PCBPrimitveHeader`
     - 
   * - Location
     - 8
     - :ref:`PCBCoordinate`
     - 
   * - SizeTop
     - 8
     - :ref:`PCBCoordinate`
     - 
   * - SizeMiddle
     - 8
     - :ref:`PCBCoordinate`
     - 
   * - SizeBottom
     - 8
     - :ref:`PCBCoordinate`
     - 
   * - HoleSize
     - 4
     - :ref:`Int32`
     - 
   * - ShapeTop
     - 1
     - :ref:`PCBPadShape`
     - 
   * - ShapeMiddle
     - 1
     - :ref:`PCBPadShape`
     - 
   * - ShapeBottom
     - 1
     - :ref:`PCBPadShape`
     - 
   * - Rotation
     - 8
     - :ref:`Double`
     - 
   * - IsPlated
     - 1
     - :ref:`Boolean`
     - 
   * - *Unknown constant*
     - 1 
     - :ref:`Byte`
     - Check Value #91 == 0?
   * - StackMode
     - 1
     - :ref:`PCBStackMode`
     - 
   * - *Unknown*
     - 1
     - :ref:`Byte`
     - 
   * - *Unknown*
     - 2 * 4
     - :ref:`Int32`
     - 
   * - *Unknown constant*
     - 1
     - :ref:`Byte`
     - Check Value #102 == 4?
   * - *Unknown*
     - 3 * 4
     - :ref:`Uint32`
     - 
   * - PasteMaskExpansion
     - 4
     - :ref:`Int32`
     - 
   * - SolderMaskExpansion
     - 4
     - :ref:`Int32`
     - 
   * - *Unknown*
     - 7
     - :ref:`Byte`
     - 
   * - PasteMaskExpansionManual
     - 1
     - :ref:`Byte`
     - 
   * - SolderMaskExpansionManual
     - 1
     - :ref:`Byte`
     - 
   * - *Unknown*
     - 3
     - :ref:`Byte`
     - 
   * - *Unknown*
     - 4
     - :ref:`Uint32`
     - 
   * - JumperId
     - 2
     - :ref:`Int16`
     - 
   * - *Unknown*
     - 2
     - :ref:`Int16`
     - 

Second block on information:

.. list-table:: 
   :header-rows: 1
   :widths: auto

   * - **Name**
     - **Size (Bytes)**
     - **Datatype**
     - **Comment**
   * - Pad X Size of Middle Layers
     - 29 * 4
     - :ref:`Int32`
     - Needs to be combined into array of :code:`SizeMiddleLayers`
   * - Pad Y Size of Middle Layers
     - 29 * 4
     - :ref:`Int32`
     - Needs to be combined into array of :code:`SizeMiddleLayers`
   * - SizeMiddleLayers
     - 
     - :ref:`PCBCoordinate`
     - Merge of previous fields
   * - ShapeLayers
     - 30 * 1
     - :ref:`PCBPadShape`
     - 
   * - *Unknown*
     - 1
     - :ref:`Byte`
     - 
   * - HoleShape
     - 1
     - :ref:`PCBHoleShape`
     - 
   * - HoleSlotLength
     - 4
     - :ref:`Int32`
     - 
   * - HoleRotation
     - 8
     - :ref:`Double`
     - 
   * - Offset X from Hole Center
     - 32 * 4
     - :ref:`Int32`
     - Needs to be combined into array of :code:`OffsetsFromHoleCenter`
   * - Offset Y from Hole Center
     - 32 * 4
     - :ref:`Int32`
     - Needs to be combined into array of :code:`OffsetsFromHoleCenter`
   * - OffsetsFromHoleCenter
     - 
     - :ref:`PCBCoordinate`
     - Merge of previous fields
   * - HasRoundedRect
     - 1
     - :ref:`Boolean`
     - 
   * - Shape Layers
     - 32 * 1
     - :ref:`Byte`
     - Use only if :code:`HasRoundedRect`, otherwise ignore
   * - CornerRadiusPercentage
     - 32 * 1
     - :ref:`Byte`
     - 

.. _PCBPrimitive03:

ID 3 - Via
-----------------

Represents a footprint via primitive. Contains only one :ref:`Block` with the following data:

.. list-table:: 
   :header-rows: 1
   :widths: auto

   * - **Name**
     - **Size (Bytes)**
     - **Datatype**
     - **Comment**
   * - Primitive Header
     - 13
     - :ref:`PCBPrimitveHeader`
     - 
   * - Location
     - 8
     - :ref:`PCBCoordinate`
     - 
   * - Diameter
     - 4
     - :ref:`Int32`
     - 
   * - HoleSize
     - 4
     - :ref:`Int32`
     - 
   * - FromLayer
     - 1
     - :ref:`Byte`
     - 
   * - ToLayer
     - 1
     - :ref:`Byte`
     - 
   * - *Unknown*
     - 1
     - :ref:`Byte`
     - 
   * - ThermalReliefAirGapWidth
     - 4
     - :ref:`Int32`
     - 
   * - ThermalReliefConductors
     - 1
     - :ref:`Byte`
     - 
   * - *Unknown*
     - 3 * 4
     - :ref:`Int32`
     - 
   * - SolderMaskExpansion
     - 4
     - :ref:`Int32`
     - 
   * - *Unknown*
     - 8 * 4
     - :ref:`Int32`
     - 
   * - SolderMaskExpansionManual
     - 1
     - :ref:`Byte`
     - 
   * - *Unknown*
     - 1
     - :ref:`Byte`
     - 
   * - *Unknown*
     - 2
     - :ref:`Int16`
     - 
   * - *Unknown*
     - 4
     - :ref:`Int32`
     - 
   * - DiameterStackMode
     - 1
     - :ref:`PCBStackMode`
     - 
   * - Diameter
     - 32 * 4
     - :ref:`Int32`
     - Iterate for each Layer
   * - *Unknown*
     - 2
     - :ref:`Int16`
     - 
   * - *Unknown*
     - 4
     - :ref:`Int32`
     - 

.. _PCBPrimitive04:

ID 4 - Track
----------------

Represents a footprint track primitive. Contains only one :ref:`Block` with the following data:

.. list-table:: 
   :header-rows: 1
   :widths: auto

   * - **Name**
     - **Size (Bytes)**
     - **Datatype**
     - **Comment**
   * - Primitive Header
     - 13
     - :ref:`PCBPrimitveHeader`
     - 
   * - Start
     - 8
     - :ref:`PCBCoordinate`
     - X/Y PCBCoordinate
   * - End
     - 8
     - :ref:`PCBCoordinate`
     - X/Y PCBCoordinate
   * - Width
     - 4
     - :ref:`Int32`
     - 
   * - *Unknown*
     - 3 * 1
     - :ref:`Byte`
     - 
   * - *Unknown*
     - 1
     - :ref:`Byte`
     - Only of length >= 41
   * - *Unknown*
     - 4
     - :ref:`Int32`
     - Only of length >= 41
   * - *Unknown*
     - 4
     - :ref:`Int32`
     - Only of length >= 45


.. _PCBPrimitive05:

ID 5 - String
-----------------

Represents a footprint string primitive. Structured as:

#. Information as :ref:`Block`
#. ASCII text as :ref:`PCBStringBlock`

If the variable :code:`WideStringsIndex` is set, read WideStrings

The information are structured as follows:

.. list-table:: 
   :header-rows: 1
   :widths: auto

   * - **Name**
     - **Size (Bytes)**
     - **Datatype**
     - **Comment**
   * - Primitive Header
     - 13
     - :ref:`PCBPrimitveHeader`
     - 
   * - Corner
     - 8
     - :ref:`PCBCoordinate`
     - 
   * - Height
     - 4
     - :ref:`Int32`
     - 
   * - StrokeFont
     - 2
     - :ref:`PCBTextStrokeFont`
     - 
   * - Rotation
     - 8
     - :ref:`Double`
     - 
   * - Mirrored
     - 1
     - :ref:`Boolean`
     - 
   * - StrokeWidth
     - 4
     - :ref:`Int32`
     - 
   * - *Unknown*
     - 2
     - :ref:`Int16`
     - Only of length >= 123
   * - *Unknown*
     - 1
     - :ref:`Byte`
     - Only of length >= 123
   * - TextKind
     - 1
     - :ref:`PCBTextKind`
     - Only of length >= 123
   * - FontBold
     - 1
     - :ref:`Boolean`
     - Only of length >= 123
   * - FontItalic
     - 1
     - :ref:`Boolean`
     - Only of length >= 123
   * - FontName
     - 32
     - :ref:`Byte`
     - Only of length >= 123, Unknown Definition
   * - BarcodeLRMargin
     - 4
     - :ref:`Int32`
     - Only of length >= 123
   * - BarcodeTBMargin
     - 4
     - :ref:`Int32`
     - Only of length >= 123
   * - *Unknown*
     - 24 * 1
     - :ref:`Byte`
     - Only of length >= 123
   * - FontInverted
     - 1
     - :ref:`Boolean`
     - Only of length >= 123
   * - FontInvertedBorder
     - 4
     - :ref:`Int32`
     - Only of length >= 123
   * - WideStringsIndex
     - 4
     - :ref:`Int32`
     - Only of length >= 123
   * - *Unknown*
     - 4
     - :ref:`Int32`
     - Only of length >= 123
   * - FontInvertedRect
     - 1
     - :ref:`Boolean`
     - Only of length >= 123
   * - FontInvertedRectWidth
     - 4
     - :ref:`Int32`
     - Only of length >= 123
   * - FontInvertedRectHeight
     - 4
     - :ref:`Int32`
     - Only of length >= 123
   * - FontInvertedRectJustification
     - 1
     - :ref:`PCBTextJustification`
     - Only of length >= 123
   * - FontInvertedRectTextOffset
     - 4
     - :ref:`Int32`
     - Only of length >= 123

.. _PCBPrimitive06:

ID 6 - Fill
-------------------

Represents a footprint fill primitive. Contains only one :ref:`Block` with the following data:

.. list-table:: 
   :header-rows: 1
   :widths: auto

   * - **Name**
     - **Size (Bytes)**
     - **Datatype**
     - **Comment**
   * - Primitive Header
     - 13
     - :ref:`PCBPrimitveHeader`
     - 
   * - Corner1
     - 8
     - :ref:`PCBCoordinate`
     - 
   * - Corner2
     - 8
     - :ref:`PCBCoordinate`
     - 
   * - Rotation
     - 8
     - :ref:`Double`
     - 
   * - *Unknown*
     - 4
     - :ref:`Int32`
     - Only of length >= 41
   * - *Unknown*
     - 1
     - :ref:`Byte`
     - Only of length >= 46
   * - *Unknown*
     - 4
     - :ref:`Int32`
     - Only of length >= 46


.. _PCBPrimitive11:

ID 11 - Region
-------------------

Represents a footprint region primitive. Contains only one :ref:`Block` with the following data:

.. list-table:: 
   :header-rows: 1
   :widths: auto

   * - **Name**
     - **Size (Bytes)**
     - **Datatype**
     - **Comment**
   * - Primitive Header
     - 13
     - :ref:`PCBPrimitveHeader`
     - 
   * - *Unknown*
     - 4
     - :ref:`Int32`
     - 
   * - *Unknown*
     - 1
     - :ref:`Byte`
     - 
   * - Parameters
     - 
     - :ref:`ParameterCollection`
     - 
   * - outlineSize
     - 4
     - :ref:`UInt32`
     - Number of outline points
   * - Outline X Point
     - 8
     - :ref:`Double`
     - Needs to be combined into array of :code:`Outline`
   * - Outline Y Point
     - 8
     - :ref:`Double`
     - Needs to be combined into array of :code:`Outline`
   * - Outline
     - n * 8
     - :ref:`PCBCoordinate`
     - 

.. _PCBPrimitive12:

ID 12 - Component Body
-----------------------

Represents a footprint component body primitive.




.. _SchPrimitives:

Schematic Records
=====================

.. _SchPrimitive01:

ID 1 - Component
-------------------
Set up schematic component part. Other objects, such as lines, pins and labels exist, which are “owned” by the component. The component object seems to occur before any of its child objects.

The parameters of this record are given a :ref:`SchRecord`. This collection includes the default parameters :ref:`SchCommonParameter` and the following parameters:

.. list-table:: 
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Comment**
   * - LibReference
     - :ref:`String`
     - Symbol Name
   * - ComponentDescription
     - :ref:`String`
     - *optional* Symbol Description
   * - PartCount
     - :ref:`Int32`
     - Number of separated parts within component + 1
   * - AllPinCount
     - :ref:`Int32`
     - Number of Pins
   * - DisplayModeCount
     - :ref:`Int32`
     - Number of alternative symbols for part

.. _SchPrimitive02:

ID 2 - Pin
-------------------
Component pin, including line, name and number.

The parameters of this record are given a :ref:`SchRecord`. This collection includes the default parameters :ref:`SchCommonParameter` as binary type :ref:`SchBinaryPin`. Some additional parameter are stored in a seperate


 and the following parameters:

.. list-table:: 
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Comment**
   * - Symbol_InnerEdge
     - :ref:`SchPinSymbol`
     - see ID 3 - IEEE Symbol
   * - Symbol_OuterEdge
     - :ref:`SchPinSymbol`
     - see ID 3 - IEEE Symbol
   * - Symbol_Inside
     - :ref:`SchPinSymbol`
     - see ID 3 - IEEE Symbol
   * - Symbol_Outside
     - :ref:`SchPinSymbol`
     - see ID 3 - IEEE Symbol
   * - Symbol_LineWdith
     - :ref:`SchLineWidth`
     -
   * - Name
     - :ref:`String`
     -
   * - Designator
     - :ref:`String`
     - 
   * - Description
     - :ref:`String`
     - 
   * - FormalType
     - :ref:`Int32`
     - 
   * - Electrical
     - :ref:`SchPinElectricalType`
     - 
   * - PinConglomerate
     - :ref:`SchPinFlags`
     - 
   * - PinLength; PinLength_Frac
     - :ref:`SchCoordinate`
     - 

.. _SchPrimitive03:

ID 3 - IEEE Symbol
-------------------
Located near some component pins (see ID 2 - Pin)

The parameters of this record are given a :ref:`SchRecord`. This collection includes the default parameters :ref:`SchCommonParameter` and the following parameters:

.. list-table:: 
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Comment**
   * - Symbol
     - :ref:`SchPinSymbol`
     - 
   * - IsMirrored
     - :ref:`Boolean`
     - 
   * - LineWidth
     - :ref:`SchLineWidth`
     -
   * - ScaleFactor
     - :ref:`Int32`
     -

.. _SchPrimitive04:

ID 4 - Label
-------------------
Text Note

The parameters of this record are given a :ref:`SchRecord`. This collection includes the default parameters :ref:`SchCommonParameter` and the following parameters:

.. list-table:: 
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Comment**
   * - Orientation
     - :ref:`SchTextOrientation`
     - 
   * - Justification
     - :ref:`SchTextJustification`
     - 
   * - FontId
     - :ref:`Int32`
     -
   * - Text
     - :ref:`String`
     -
   * - IsMirrored
     - :ref:`Boolean`
     -
   * - IsHidden
     - :ref:`Boolean`
     -

.. _SchPrimitive05:

ID 5 - Bezier
-------------------
Bezier curve for component symbol. Similar structure as ID 6 - Polyline.

The parameters of this record are given a :ref:`SchRecord`. This collection includes the default parameters :ref:`SchCommonParameter` and the following parameters:

.. list-table:: 
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Comment**
   * - LineStyle
     - :ref:`SchLineStyle`
     - 
   * - LineWidth
     - :ref:`SchLineWidth`
     - 
   * - IsSolid
     - :ref:`Boolean`
     - 
   * - LocationCount
     - :ref:`Int32`
     - Number of vertices
   * - X; X_Frac; Y; Y_Frac
     - :ref:`SchCoordinatePoint`
     - 
   * - Transparent
     - :ref:`Boolean`
     - 

.. _SchPrimitive06:

ID 6 - Polyline
-------------------
Polyline for component symbol. Similar structure as ID 5 - Bezier.

The parameters of this record are given a :ref:`SchRecord`. This collection includes the default parameters :ref:`SchCommonParameter` and the following parameters:

.. list-table:: 
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Comment**
   * - LineStyle
     - :ref:`SchLineStyle`
     - 
   * - LineWidth
     - :ref:`SchLineWidth`
     - 
   * - IsSolid
     - :ref:`Boolean`
     - 
   * - LocationCount
     - :ref:`Int32`
     - Number of vertices
   * - X; X_Frac; Y; Y_Frac
     - :ref:`SchCoordinatePoint`
     - 
   * - Transparent
     - :ref:`Boolean`
     - 
   * - StartLineShape
     - :ref:`SchLineShape`
     - 
   * - EndLineShape
     - :ref:`SchLineShape`
     - 
   * - LineShapeSize
     - :ref:`Int32`
     - 

.. _SchPrimitive07:

ID 7 - Polygon
-------------------
Polygon for component symbol. Similar structure as ID 6 - Polyline.

The parameters of this record are given a :ref:`SchRecord`. This collection includes the default parameters :ref:`SchCommonParameter` and the following parameters:

.. list-table:: 
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Comment**
   * - LineWidth
     - :ref:`SchLineWidth`
     - 
   * - IsSolid
     - :ref:`Boolean`
     - 
   * - LocationCount
     - :ref:`Int32`
     - Number of vertices
   * - X; X_Frac; Y; Y_Frac
     - :ref:`SchCoordinatePoint`
     - 
   * - Transparent
     - :ref:`Boolean`
     - 

.. _SchPrimitive08:

ID 8 - Ellipse
-------------------
Ellipse for component symbol. Inherits Circle/Pie properties

The parameters of this record are given a :ref:`SchRecord`. This collection includes the default parameters :ref:`SchCommonParameter` and the following parameters:

.. list-table:: 
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Comment**
   * - Radius
     - :ref:`SchCoordinate`
     - one coordinate for X-direction
   * - SecondaryRadius
     - :ref:`SchCoordinate`
     - one coordinate for Y-direction
   * - IsSolid
     - :ref:`Boolean`
     - 
   * - Linewidth
     - :ref:`SchLineWidth`
     - 
   * - X; X_Frac; Y; Y_Frac
     - :ref:`SchCoordinate`
     - 
   * - Transparent
     - :ref:`Boolean`
     - 

.. _SchPrimitive09:

ID 9 - Pie
-------------------
Same as Arc component (ID = 12). Start Angle is 0 degree and End Angle is 360 Degree


.. _SchPrimitive10:

ID 10 - Rounded Rectangle
--------------------------
Similar to Rectangle for component symbol. One corner radius paraneter added

The parameters of this record are given a :ref:`SchRecord`. This collection includes the default parameters :ref:`SchCommonParameter` and the following parameters:

.. list-table:: 
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Comment**
   * - Corner
     - :ref:`SchCoordinatePoint`
     - Second Coordinate
   * - IsSolid
     - :ref:`Boolean`
     - 
   * - Linewidth
     - :ref:`SchLineWidth`
     - 
   * - Transparent
     - :ref:`Boolean`
     - 
   * - CornerXRadius
     - :ref:`SchCoordinate`
     - 
   * - CornerYRadius
     - :ref:`SchCoordinate`
     - 

.. _SchPrimitive11:

ID 11 - Elliptical Arc
-----------------------
Elliptical Arc for component symbol. Inherits Arc properties.

The parameters of this record are given a :ref:`SchRecord`. This collection includes the default parameters :ref:`SchCommonParameter` and the following parameters:

.. list-table:: 
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Comment**
   * - Radius
     - :ref:`SchCoordinate`
     - one coordinate for X-direction
   * - SecondaryRadius
     - :ref:`SchCoordinate`
     - one coordinate for Y-direction
   * - StartAngle
     - :ref:`Double`
     - 
   * - EndAngle
     - :ref:`Double`
     - 
   * - Linewidth
     - :ref:`SchLineWidth`
     - 
   * - Transparent
     - :ref:`Boolean`
     - 
.. _SchPrimitive12:
  
ID 12 - Arc
-----------------------
Arc for component symbol.

The parameters of this record are given a :ref:`SchRecord`. This collection includes the default parameters :ref:`SchCommonParameter` and the following parameters:

.. list-table:: 
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Comment**
   * - Radius
     - :ref:`SchCoordinate`
     - one coordinate for X-direction
   * - StartAngle
     - :ref:`Double`
     - 
   * - EndAngle
     - :ref:`Double`
     - 
   * - Linewidth
     - :ref:`SchLineWidth`
     - 
   * - Transparent
     - :ref:`Boolean`
     - 

.. _SchPrimitive13:

ID 13 - Line
-----------------------
Line for component symbol

The parameters of this record are given a :ref:`SchRecord`. This collection includes the default parameters :ref:`SchCommonParameter` and the following parameters:

.. list-table:: 
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Comment**
   * - Corner
     - :ref:`SchCoordinatePoint`
     - 
   * - LineStyle
     - :ref:`SchLineStyle`
     - 
   * - Linewidth
     - :ref:`SchLineWidth`
     - 

.. _SchPrimitive14:

ID 14 - Rectangle
-----------------------
Rectangle for component symbol.

The parameters of this record are given a :ref:`SchRecord`. This collection includes the default parameters :ref:`SchCommonParameter` and the following parameters:

.. list-table:: 
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Comment**
   * - Corner
     - :ref:`SchCoordinatePoint`
     - Second Coordinate
   * - IsSolid
     - :ref:`Boolean`
     - 
   * - Linewidth
     - :ref:`SchLineWidth`
     - 
   * - Transparent
     - :ref:`Boolean`
     - 

.. _SchPrimitive34:

ID 34 - Designator
-----------------------
Designator record for component symbol.

The parameters of this record are given a :ref:`SchRecord`. This collection includes the default parameters :ref:`SchCommonParameter` and the following parameters:

.. list-table:: 
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Comment**
   * - FontId
     - :ref:`Int32`
     -
   * - Text
     - :ref:`String`
     -
   * - IsMirrored
     - :ref:`Boolean`
     -
   * - IsHidden
     - :ref:`Boolean`
     -

.. _SchPrimitive41:

ID 41 - Parameter
-----------------------
Parameter record for component symbol.

The parameters of this record are given a :ref:`SchRecord`. This collection includes the default parameters :ref:`SchCommonParameter` and the following parameters:

.. list-table:: 
   :header-rows: 1

   * - **Parameter**
     - **Datatype**
     - **Comment**
   * - FontId
     - :ref:`Int32`
     -
   * - Name
     - :ref:`String`
     -
   * - Text
     - :ref:`String`
     -
   * - IsMirrored
     - :ref:`Boolean`
     -
   * - IsHidden
     - :ref:`Boolean`
     -