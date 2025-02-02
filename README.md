[![Build and Release on GitHub](https://github.com/ChrisHoyer/pyAltiumLib/actions/workflows/publish-github.yml/badge.svg)](https://github.com/ChrisHoyer/pyAltiumLib/actions/workflows/publish-github.yml)
![GitHub Release](https://img.shields.io/github/v/release/ChrisHoyer/pyAltiumLib)
[![Build and Release on PyPi](https://github.com/ChrisHoyer/pyAltiumLib/actions/workflows/publish-pypi.yml/badge.svg)](https://github.com/ChrisHoyer/pyAltiumLib/actions/workflows/publish-pypi.yml)
[![PyPI Release](https://img.shields.io/pypi/v/pyaltiumlib.svg)](https://pypi.org/project/pyaltiumlib/)
[![Documentation Status](https://readthedocs.org/projects/pyaltiumlib/badge/?version=latest)](https://pyaltiumlib.readthedocs.io/latest)

# pyAltiumLib

PyAltiumLib is a tool to read Altium Designer library files. The included components are extracted. Metadata such as the description and the name of the component can be listed. It is also possible to visualize the component using the svgwrite package.

See full documentation here: [ReadTheDocs](https://pyaltiumlib.readthedocs.io/)

## Example - Read the File and Retrieve Components

Load the file and retrieve the list of components.

```python
import pyaltiumlib

# Path to the .schlib or .pcblib file
filepath = "Libfile.schlib"

# Load File
LibFile = pyaltiumlib.read(filepath)

# Read Meta Data
json = LibFile.read_meta()

# Get a List of All Components
all_parts = LibFile.list_parts()
```

## Example - Render Components as SVG

Render each component as an SVG file. The components are saved as individual SVG files in the img_sch directory.

```python
import svgwrite

# Iterate over all components to draw them
for partname in all_parts:

    # Choose element
    Component = LibFile.get_part(partname)

    # Create a new image with a white background
    dwg = svgwrite.Drawing(f"img_sch/{partname}.svg", size=(400, 400))

    # Draw component on svg drawing with size 400px 400px
    Component.draw_svg(dwg, 400, 400)

    # Save the SVG
    dwg.save()
```