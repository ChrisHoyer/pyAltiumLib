Common Data Types
#################

.. _Block:
Block
======
A `Block` represents a data structure that contains the length of the block and the data of the block itself. The data can be in different formats, e.g. string or byte or a composite. The first 4 bytes are little-endian and define the length of the block.

.. _ParameterCollection:
Parameter Collection
=====================
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
==========================
Color as defined in GDI+ structures.



.. _UInt32:
Unsigned Integer (32-bit)
==========================
Represents a 32-bit unsigned integer.

**Schematic Record:** Default value if property is missing seems to be :code:`0`.

.. _Int32:
Signed Integer (32-bit)
==========================
Represents a 32-bit signed integer.

**Schematic Record:** Default value if property is missing seems to be :code:`0`.

.. _Int16:
Signed Integer (16-bit)
==========================
Represents a 16-bit signed integer.

**Schematic Record:** Default value if property is missing seems to be :code:`0`.

.. _Double:
Double
==========================
Represents a 64-bit floating-point number. Typically three decimal places.

**Schematic Record:** property omitted if property is missing.

.. _Boolean:
Boolean
==========================
Represents a boolean value (True or False).

**Schematic Record:** Either :code:`T` for true or :code:`F` for false. When false, the property is often omitted, rather than explicitly set to false.

.. _Byte:
Byte
==========================
Represents a single byte (8 bits).

.. _String:
String
==========================
Represents a ASCII string.