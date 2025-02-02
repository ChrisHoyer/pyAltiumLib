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

- **Python Standard Libraries**: `sys`, `os`, `math`, `typing`
- **External Libraries**:
    - `olefile` - for reading Altium library files
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

