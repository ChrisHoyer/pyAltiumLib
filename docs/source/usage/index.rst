#############################
Installation & Contributing
#############################

Installation
============
*WIP: needs to be available via pip*

For now just refer to the module folder located in :code:`PyAltiumLib/src`

Dependencies:

- :code:`sys, os`
- :code:`math, svgwrite` - to render drawings
- :code:`json` - to have a json dump output

Usage Instructions
===================

This guide provides instructions on how to use the library to read a file, retrieve components, and render them as SVG.

Ensure the package is already installed. Additionally, for rendering components as SVG, the `svgwrite` package must be installed.

Installation of `svgwrite` (if not already installed):

.. code-block:: bash
    
    pip install svgwrite


Read the File and Retrieve Components
----------------------------------------

Load the file and retrieve the list of components.

.. code-block:: python

    import pyaltiumlib

    # path to the .schlib or .pcblib file
    filepath = "Libfile.schlib"

    # Load File
    LibFile = pyaltiumlib.read(filepath)

    # Receive Component List as JSON
    json = LibFile.toJSON()

    # Get a List of All Components
    all_parts = LibFile.ListParts()

Render Components as SVG
----------------------------------------

Render each component as an SVG file. The components are saved as individual SVG files in the `img_sch` directory.

.. code-block:: python

    import svgwrite

    # iterate all components to draw them
    for partname in all_parts:

        # Choose element
        Component = LibFile.GetPart(partname)

        # Create a new image with a white background
        dwg = svgwrite.Drawing(f"img_sch/{partname}.svg", size=(400, 400))

        # Draw component on svg drawing with size 400px 400px
        Component.draw_svg(dwg, 400, 400)

        # Save the SVG
        dwg.save()


Contributing
============
*WIP*


