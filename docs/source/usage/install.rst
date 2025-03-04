Installation & Usage Guide
**************************

Installation
============

To install `pyaltiumlib`, use the following command:

.. code-block:: bash

    pip install pyaltiumlib

Dependencies  
--------------

The following dependencies are automatically installed with `pyaltiumlib`:

- **Python Standard Libraries**: `sys`, `os`, `io`, `math`, `typing`, `logging`
- **External Libraries**:
    - `olefile` - for reading ole files (Altium library file container)
    - `svgwrite` - for rendering schematic and PCB drawings


Usage
======

Reading an Altium Library File  
---------------------------------

Load a `.schlib` or `.pcblib` file and retrieve the list of components.

.. code-block:: python

    import pyaltiumlib

    # Define the file path to the library
    filepath = "Libfile.schlib"

    # Load the library file
    LibFile = pyaltiumlib.read(filepath)

    # Retrieve metadata
    metadata = LibFile.read_meta()

    # Get a list of all components
    all_parts = LibFile.list_parts()

Or reading directly the binary io stream

.. code-block:: python

    import pyaltiumlib

    # Fetch the binary stream of the file
    libfile_bytes = ....
    libfile_obj = io.BytesIO(libfile_bytes)

    # Load the library file
    # filepath is still required to identify and identicate the correct file
    LibFile = LibFile = altlib.read(filepath, libfile_obj)

    # Retrieve metadata
    metadata = LibFile.read_meta()

    # Get a list of all components
    all_parts = LibFile.list_parts()



Rendering Components as SVG  
---------------------------------

Render each component as an SVG and save them in the `img_sch` directory.

.. code-block:: python

    import svgwrite

    # Iterate over all components and generate SVG images
    for partname in all_parts:

        # Retrieve the component
        Component = LibFile.get_part(partname)

        # Create an SVG drawing
        dwg = svgwrite.Drawing(f"img_sch/{partname}.svg", size=(400, 400))

        # Draw the component within a 400x400 px canvas
        Component.draw_svg(dwg, 400, 400)

        # Save the generated SVG file
        dwg.save()

