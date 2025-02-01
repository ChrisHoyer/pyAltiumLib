Library Classes
*******************

Dynamic Library Factory
============================

.. automodule:: pyaltiumlib
   :members:
   :undoc-members:
   :special-members: __init__

Generic Library File (Base)
=================================

.. autoclass:: pyaltiumlib.base.GenericLibFile

    .. autoattribute:: LibType
    .. autoattribute:: LibHeader
    .. autoattribute:: FilePath
    .. autoattribute:: ComponentCount
    .. autoattribute:: Parts

    .. automethod:: pyaltiumlib.base.GenericLibFile.read_meta
    .. automethod:: pyaltiumlib.base.GenericLibFile.list_parts
    .. automethod:: pyaltiumlib.base.GenericLibFile.get_part

Schematic Library File (SchLib)
===============================

.. autoclass:: pyaltiumlib.schlib.lib.SchLib

PCB Library File (PCBLib)
==========================

.. autoclass:: pyaltiumlib.pcblib.lib.PcbLib

