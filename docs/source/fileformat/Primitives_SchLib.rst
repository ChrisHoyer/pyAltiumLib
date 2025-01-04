 .. _SchPrimitives:
Schematic Records
##################

ID 1 - Component
****************************
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


ID 2 - Pin
****************************
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


ID 3 - IEEE Symbol
****************************
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



ID 4 - Label
****************************
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

ID 5 - Bezier
****************************
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

ID 6 - Polyline
****************************
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

ID 7 - Polygon
****************************
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

ID 8 - Ellipse
****************************
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

ID 9 - Pie
****************************
Same as Arc component (ID = 12). Start Angle is 0 degree and End Angle is 360 Degree


ID 10 - Rounded Rectangle
****************************
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

ID 11 - Elliptical Arc
****************************
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

  
ID 12 - Arc
****************************
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

ID 13 - Line
****************************
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

  
ID 14 - Rectangle
****************************
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