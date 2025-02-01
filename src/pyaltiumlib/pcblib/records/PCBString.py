from pyaltiumlib.pcblib.records.base import _GenericPCBRecord
from pyaltiumlib.datatypes import BinaryReader, Coordinate, CoordinatePoint
from pyaltiumlib.datatypes import PCBTextJustification, PCBTextKind
from typing import Tuple
import logging

# Configure logging
logger = logging.getLogger(__name__)

class PcbString(_GenericPCBRecord):
    """
    Represents a text string in an Altium PCB library.
    
    Attributes:
        corner1 (CoordinatePoint): The reference corner of the text.
        height (Coordinate): The height of the text.
        stroke_font (int): The stroke font type.
        rotation (float): The rotation angle of the text in degrees.
        mirrored (bool): Whether the text is mirrored.
        stroke_width (Coordinate): The stroke width of the text.
        text_kind (PCBTextKind): The type of text (e.g., standard, barcode).
        font_bold (bool): Whether the font is bold.
        font_italic (bool): Whether the font is italic.
        font_name (str): The name of the font.
        barcode_margin_lr (int): Left/right margin for barcode text.
        barcode_margin_tb (int): Top/bottom margin for barcode text.
        font_inverted (bool): Whether the text is inverted.
        font_inverted_border (int): The border width for inverted text.
        widestring_index (int): Index for wide string support.
        font_inverted_rect (bool): Whether the text has an inverted rectangle.
        font_inverted_rect_width (Coordinate): Width of the inverted rectangle.
        font_inverted_rect_height (Coordinate): Height of the inverted rectangle.
        font_inverted_rect_justification (PCBTextJustification): Justification of the inverted rectangle.
        font_inverted_rect_text_offset (int): Text offset within the inverted rectangle.
        text (str): The actual text content.
        alignment (Dict): Alignment and rotation metadata for rendering.
    """

    def __init__(self, parent, stream):
        """
        Initialize a PCB string with a parent object and a binary data stream.
        
        Args:
            parent: The parent object (usually a footprint or component).
            stream: A binary stream containing the string data.
        """
        super().__init__(parent)
        self.parse(stream)

    def __repr__(self) -> str:
        """Return a string representation of the PCB string."""
        variables = ', '.join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}({variables})"

    def parse(self, stream) -> None:
        """
        Parse the binary stream to extract string data.
        
        Args:
            stream: A binary stream containing the string data.
        
        Raises:
            ValueError: If the stream is invalid or incomplete.
        """
        try:
            block = BinaryReader.from_stream(stream)
            string = BinaryReader.from_stream(stream)

           # Read Block 
            if block.has_content():
                self.read_common( block.read(13) )
                self.corner1 = block.read_bin_coord()
                self.height = Coordinate.parse_bin( block.read(4) ) 
                self.stroke_font = block.read_int16()
                self.rotation = block.read_double()
                self.mirrored = bool(block.read_byte())
                self.stroke_width = Coordinate.parse_bin( block.read(4) ) 
                
                if block.length() >= 123:
                    
                    block.read_int16() # Unknown
                    block.read_byte() # Unknown
                    
                    self.text_kind = PCBTextKind( block.read_int8() )
                    self.font_bold = block.read_byte()
                    self.font_italic = block.read_byte()
                    self.font_name = block.read_unicode_text()
                    self.barcode_margin_lr = block.read_int32()
                    self.barcode_margin_tb = block.read_int32()                
                    
                    block.read_int32() # Unknown
                    block.read_int32() # Unknown
                    block.read_byte() # Unknown
                    block.read_byte() # Unknown
                    block.read_int32() # Unknown
                    block.read_int16() # Unknown
                    block.read_int32() # Unknown
                    block.read_int32() # Unknown  
                    
                    self.font_inverted = block.read_byte()
                    self.font_inverted_border = block.read_int32()
                    self.widestring_index = block.read_int32()
                    
                    block.read_int32() # Unknown
                    
                    self.font_inverted_rect = block.read_byte()
                    self.font_inverted_rect_width = Coordinate.parse_bin(block.read(4))
                    self.font_inverted_rect_height = Coordinate.parse_bin(block.read(4))
                    self.font_inverted_rect_justification = PCBTextJustification( block.read_int8() )              
                    self.font_inverted_rect_text_offset = block.read_int32() 
                    
                    
            if string.has_content():
                self.text = string.read_string_block()
                
        except Exception as e:
            logger.error(f"Failed to parse PCB string: {str(e)}")
            raise

    def get_bounding_box(self) -> Tuple[CoordinatePoint, CoordinatePoint]:
        """
        Calculate the bounding box for the text, including rotation and alignment.
        
        Returns:
            Tuple[CoordinatePoint, CoordinatePoint]: The minimum and maximum points
            of the bounding box, accounting for rotation and alignment.
        """
        try:
            self.alignment = {
                "vertical": self.font_inverted_rect_justification.get_vertical(),
                "horizontal": self.font_inverted_rect_justification.get_horizontal(),
                "rotation": -self.rotation,
                "anchor": self.corner1.copy()
            }

            # Calculate bounding box corners
            left_top = self.corner1.copy()
            right_bot = self.corner1.copy()
            left_top.y -= self.font_inverted_rect_height
            right_bot.x += self.font_inverted_rect_width

            # Adjust anchor point based on vertical alignment
            if self.alignment["vertical"] == "text-after-edge":
                self.alignment["anchor"].y -= self.font_inverted_rect_height
                left_top.y -= self.font_inverted_rect_height
                right_bot.y -= self.font_inverted_rect_height
            elif self.alignment["vertical"] == "central":
                self.alignment["anchor"].y -= self.font_inverted_rect_height / 2
            elif self.alignment["vertical"] == "text-before-edge":
                self.alignment["anchor"].y = self.corner1.y
                left_top.y += self.font_inverted_rect_height
                right_bot.y += self.font_inverted_rect_height

            # Adjust anchor point based on horizontal alignment
            if self.alignment["horizontal"] == "end":
                self.alignment["anchor"].x += self.font_inverted_rect_width
            elif self.alignment["horizontal"] == "middle":
                self.alignment["anchor"].x += self.font_inverted_rect_width / 2
            elif self.alignment["horizontal"] == "start":
                self.alignment["anchor"].x = self.corner1.x

            # Apply rotation to anchor and bounding box corners
            self.alignment["anchor"] = self.alignment["anchor"].rotate(self.corner1, -self.rotation)
            left_top = left_top.rotate(self.corner1, -self.rotation)
            right_bot = right_bot.rotate(self.corner1, -self.rotation)

            return [left_top, right_bot]
        except Exception as e:
            logger.error(f"Error calculating bounding box: {str(e)}")
            return self.corner1, self.corner1

    def draw_svg(self, dwg, offset: CoordinatePoint, zoom: float) -> None:
        """
        Render the text as an SVG element.
        
        Args:
            dwg: The SVG drawing object.
            offset (CoordinatePoint): The offset for drawing.
            zoom (float): The zoom factor for scaling.
        
        Raises:
            ValueError: If the layer or drawing context is invalid.
        """
        try:
            # Calculate scaled and offset coordinates
            insert = (self.alignment["anchor"] * zoom) + offset
            
            # Get the layer color
            layer = self.get_layer_by_id(self.layer)
            if layer is None:
                logger.error(f"Invalid layer ID: {self.layer}")

            # Determine font
            font = self.text_kind.get_font() if self.text_kind == PCBTextKind(0) else self.font_name

            # Draw the text as an SVG element
            drawing_primitive = dwg.text(
                self.text,
                font_size=int(self.height * zoom),
                font_family=font,
                insert=insert.to_int_tuple(),
                fill=layer.color.to_hex(),
                dominant_baseline=self.alignment["vertical"],
                text_anchor=self.alignment["horizontal"],
                transform=f"rotate({self.alignment['rotation']} {int(insert.x)} {int(insert.y)})"
            )

            # Add the text to the appropriate drawing layer
            self.Footprint._drawing_layer[self.layer].add(drawing_primitive)
        except Exception as e:
            logger.error(f"Failed to draw PCB string: {str(e)}")
            raise