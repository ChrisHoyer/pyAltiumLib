Schematic Library (.schlib)
############################

The `.schlib` file format stores schematic symbols. It is based on OLE (Object Linking and Embedding) format, a compound document standard from Microsoft. 

::

   <file.schlib>/
   ├── FileHeader
   ├── Storage
   ├── <symbol>/
   │   ├── PinFrac
   │   ├── PinSymbolLineWidth
   │   ├── PinWideText
   │   ├── PinTextData
   │   ├── PinFunctionData
   │   └── Data
   └── ...

Streams
*********

- Structure of :code:`FileHeader`:
   #. Library header as :ref:`ParameterCollection`

Container <symbol>
********************

A container for each individual symbol. The naming of this container has some limitations due to the compound document standard. The maximum text length is 31, container names longer than 31 will be truncated. Also, if a :code:`/` is used in the name, it will be replaced by a :code:`_`.

- Structure of :code:`<symbol>/Data`:
   #. List of Records/Primitives

      #. Records/Primitive as :ref:`SchPrimitives`


*Work in Progess*:

Optional structures: only available if symbol has specific element of structure.

- Structure of :code:`<symbol>/PinFrac`:

- Structure of :code:`<symbol>/PinSymbolLineWidth`:

- Structure of :code:`<symbol>/PinWideText`:

- Structure of :code:`<symbol>/PinTextData`:

- Structure of :code:`<symbol>/PinFunctionData`:
