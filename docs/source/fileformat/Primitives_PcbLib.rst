.. _PCBPrimitives:
PCB Primitives
################

ID 1 - Arc
*******************

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


ID 2 - Pad
*****************

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

ID 3 - Via
*******************

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


ID 4 - Track
******************

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


ID 5 - String
*******************

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


ID 6 - Fill
*****************

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


ID 11 - Region
*******************

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


ID 12 - Component Body
*************************

Represents a footprint component body primitive. Contains only one :ref:`Block` with the following data:

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

The following parameters are included in the :ref:`ParameterCollection`

 -  V7_LAYER
 -  NAME
 -  KIND
 -  SUBPOLYINDEX
 -  UNIONINDEX
 -  ARCRESOLUTION
 -  ISSHAPEBASED
 -  STANDOFFHEIGHT
 -  OVERALLHEIGHT
 -  BODYPROJECTION
 -  ARCRESOLUTION
 -  BODYCOLOR3D
 -  BODYOPACITY3D
 -  IDENTIFIER
 -  TEXTURE
 -  TEXTURECENTERX
 -  TEXTURECENTERY
 -  TEXTURESIZEX
 -  TEXTURESIZEY
 -  TEXTUREROTATION
 -  MODELID
 -  MODEL.CHECKSUM
 -  MODEL.EMBED
 -  MODEL.2D.X
 -  MODEL.2D.Y
 -  MODEL.2D.ROTATION
 -  MODEL.3D.ROTX
 -  MODEL.3D.ROTY
 -  MODEL.3D.ROTZ
 -  MODEL.3D.DZ
 -  MODEL.SNAPCOUNT
 -  MODEL.MODELTYPE
