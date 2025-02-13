from pyaltiumlib.pcblib.records.base import _GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader, Coordinate, CoordinatePoint
from typing import Tuple

# Configure logging
import logging
logger = logging.getLogger(__name__)

class PcbArc(_GenericPCBRecord):
    """
    Represents a PCB Arc in an Altium PCB library.
    
    Attributes:
        start (CoordinatePoint): The starting point of the track.
        end (CoordinatePoint): The ending point of the track.
        linewidth (Coordinate): The width of the track.
        layer (int): The layer on which the track is drawn.
    """

    def __init__(self, parent, stream):
        """
        Initialize a PCB track with a parent object and a binary data stream.
        """
        super().__init__(parent)
        self._parse(stream)

    def __repr__(self) -> str:
        """Return a string representation of the PCB track."""
        return f"PCBArc"

    def _parse(self, stream) -> None:
        """
        Parse the binary stream to extract track data.
        """
        try:
            block = BinaryReader.from_stream(stream)
            
            if block.has_content():
                
                if block.length() > 67:
                # TODO: ERROR. To long!
                    return
                
                # Read common properties (e.g., layer, flags)
                self.read_common(block.read(13))
                
                # Read track-specific properties
                self.location = block.read_bin_coord()
                self.radius =  Coordinate.parse_bin(block.read(4))
                self.angle_start = block.read_double() 
                self.angle_end = block.read_double() 
                self.linewidth = Coordinate.parse_bin(block.read(4))
                
            self.is_initialized = True
                
        except Exception as e:
            logger.error(f"Failed to parse PCB track: {str(e)}")
            raise



    def get_bounding_box(self) -> Tuple[CoordinatePoint, CoordinatePoint]:
        """
        Calculate the bounding box
        """
        start_x = self.location.x - self.radius
        start_y = self.location.y - self.radius
        end_x = self.location.x + self.radius
        end_y = self.location.y + self.radius

        min_x = min(self.location.x, start_x, end_x)
        max_x = max(self.location.x, start_x, end_x)
        min_y = min(self.location.y, start_y, end_y)
        max_y = max(self.location.y, start_y, end_y)
        
        return [CoordinatePoint(min_x, min_y), CoordinatePoint(max_x, max_y)]

    def draw_svg(self, dwg, offset: CoordinatePoint, zoom: float) -> None:
        """
        Render as svg
        """
        
        center = (self.location * zoom) + offset
        radius = self.radius * zoom
        
        # Get the layer color
        layer = self.get_layer_by_id(self.layer)
        if layer is None:
            raise ValueError(f"Invalid layer ID: {self.layer}")

        arc_path = self.get_svg_arc_path(center.to_int_tuple(),
                                         int(radius), int(radius),
                                         self.angle_start, self.angle_end)

        drawing_primitive = dwg.path(d=arc_path,
                                     fill="none",
                                     stroke=layer.color.to_hex(),
                                     stroke_width=int(self.linewidth) * zoom,
                                     stroke_linejoin="round",
                                     stroke_linecap="round")
                
        # Add the line to the appropriate drawing layer
        self.Footprint._graphic_layers[self.layer].add(drawing_primitive)


