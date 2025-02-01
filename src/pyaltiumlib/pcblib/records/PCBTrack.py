from pyaltiumlib.pcblib.records.base import _GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader, Coordinate, CoordinatePoint
from typing import Tuple
import logging

# Configure logging
logger = logging.getLogger(__name__)

class PcbTrack(_GenericPCBRecord):
    """
    Represents a PCB track (a line segment) in an Altium PCB library.
    
    Attributes:
        start (CoordinatePoint): The starting point of the track.
        end (CoordinatePoint): The ending point of the track.
        linewidth (Coordinate): The width of the track.
        layer (int): The layer on which the track is drawn.
    """

    def __init__(self, parent, stream):
        """
        Initialize a PCB track with a parent object and a binary data stream.
        
        Args:
            parent: The parent object (usually a footprint or component).
            stream: A binary stream containing the track data.
        """
        super().__init__(parent)
        self.parse(stream)

    def __repr__(self) -> str:
        """Return a string representation of the PCB track."""
        return f"PCBTrack(start={self.start}, end={self.end}, width={self.linewidth})"

    def parse(self, stream) -> None:
        """
        Parse the binary stream to extract track data.
        
        Args:
            stream: A binary stream containing the track data.
        
        Raises:
            ValueError: If the stream is invalid or incomplete.
        """
        try:
            block = BinaryReader.from_stream(stream)
            
            if block.has_content():
                # Read common properties (e.g., layer, flags)
                self.read_common(block.read(13))
                
                # Read track-specific properties
                self.start = block.read_bin_coord()  # Starting point
                self.end = block.read_bin_coord()    # Ending point
                self.linewidth = Coordinate.parse_bin(block.read(4))  # Track width
                
        except Exception as e:
            logger.error(f"Failed to parse PCB track: {str(e)}")
            raise ValueError("Invalid PCB track data")

    def get_bounding_box(self) -> Tuple[CoordinatePoint, CoordinatePoint]:
        """
        Calculate the bounding box for the track, including its width.
        
        Returns:
            Tuple[CoordinatePoint, CoordinatePoint]: The minimum and maximum points
            of the bounding box, accounting for the track's width.
        """
        try:
            half_width = float(self.linewidth) / 2
            
            # Calculate min/max coordinates, including track width
            min_x = min(float(self.start.x), float(self.end.x)) - half_width
            min_y = min(float(self.start.y), float(self.end.y)) - half_width
            max_x = max(float(self.start.x), float(self.end.x)) + half_width
            max_y = max(float(self.start.y), float(self.end.y)) + half_width
            
            return (
                CoordinatePoint(Coordinate(min_x), Coordinate(min_y)),
                CoordinatePoint(Coordinate(max_x), Coordinate(max_y))
            )
        except Exception as e:
            logger.error(f"Error calculating bounding box: {str(e)}")
            return self.start, self.end

    def draw_svg(self, dwg, offset: CoordinatePoint, zoom: float) -> None:
        """
        Render the track as an SVG line.
        
        Args:
            dwg: The SVG drawing object.
            offset (CoordinatePoint): The offset for drawing.
            zoom (float): The zoom factor for scaling.
        
        Raises:
            ValueError: If the layer or drawing context is invalid.
        """
        try:
            # Calculate scaled and offset coordinates
            start = (self.start * zoom) + offset
            end = (self.end * zoom) + offset
            
            # Get the layer color
            layer = self.get_layer_by_id(self.layer)
            if layer is None:
                raise ValueError(f"Invalid layer ID: {self.layer}")
            
            # Draw the track as an SVG line
            drawing_primitive = dwg.line(
                start=start.to_int_tuple(),
                end=end.to_int_tuple(),
                stroke=layer.color.to_hex(),
                stroke_width=int(self.linewidth) * zoom,
                stroke_linejoin="round",
                stroke_linecap="round"
            )
            
            # Add the line to the appropriate drawing layer
            self.Footprint._drawing_layer[self.layer].add(drawing_primitive)
        except Exception as e:
            logger.error(f"Failed to draw PCB track: {str(e)}")
            raise