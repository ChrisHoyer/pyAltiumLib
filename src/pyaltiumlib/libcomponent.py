from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint

import json
import logging
from typing import Dict, List, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LibComponent:
    """
   A class to represent a component in an Altium library.

   Attributes:
       LibFile: The parent library file.
       Name (str): The name of the component.
       Description (str): The description of the component.
       Records (List[Any]): A list of records in the component.
       _BoundingBoxes (List[Any]): A list of bounding boxes for the component.
       drawing_layer (Dict[int, Any]): A dictionary of drawing layers for PCB Libs.
   """
   
    def __init__(self, parent, name: str, description: str):
        """
        Initialize a LibComponent object.

        Args:
            parent: The parent library file.
            name (str): The name of the component.
            description (str): The description of the component.
        """        
        self.LibFile = parent
        self.Name = name
        self.Description = description
                    
        self.Records = [] 
        self._BoundingBoxes = []
        self.drawing_layer = {}
        
    
    def __repr__(self) -> str:
        """
        Return a JSON representation of the component.

        Returns:
            str: A JSON string representation of the component.
        """
        symbol_data = {
           "Name": self.Name,
           "Description": self.Description
           }
        
        return json.dumps(symbol_data, indent=4)
   

# =============================================================================
#     Drawing related
# =============================================================================   
 
    
    def draw_svg(self, graphic, size_x: float, size_y: float, draw_bbox: bool = False) -> None:
        """
        Draw the component as an SVG.

        Args:
            graphic: The SVG graphic object.
            size_x (float): The width of the SVG.
            size_y (float): The height of the SVG.
            draw_bbox (bool): Whether to draw bounding boxes.
        """    
        validObj = []
        for obj in self.Records:
            if hasattr(obj, 'draw_svg') and callable(getattr(obj, 'draw_svg')):
                validObj.append(obj)
            else:
                logger.warning(f"Object: {obj} has no drawing function")

        # Get Bounding box
        offset, zoom = self._autoscale( validObj, size_x, size_y)
        
        # background color
        graphic.add(graphic.rect(insert=(0, 0),
                                 size=[size_x, size_y],
                                 fill=self.LibFile._BackgroundColor.to_hex()))
        
        # Add Drawing Layer
        if hasattr(self, 'LibFile'):
            if hasattr(self.LibFile, 'Layer'):
                for x in sorted(self.LibFile.Layer, key=lambda obj: obj.drawing_order, reverse=True):
                    self.drawing_layer[x.id] = graphic.add(graphic.g(id=x.svg_layer))
                
        if draw_bbox:
            for obj in validObj:
                    obj.draw_bounding_box( graphic, offset, zoom)
            
        # Draw Primitives
        for obj in validObj:
            obj.draw_svg( graphic, offset, zoom)               


    def _autoscale(self, elements: List[Any], target_width: float, target_height: float, margin: float = 10.0) -> tuple:
        """
        Adjust the coordinates of elements to fit within the target dimensions using zoom.

        Args:
            elements (List[Any]): A list of objects with `get_bounding_box` method.
            target_width (float): Target image width.
            target_height (float): Target image height.
            margin (float): Margin around the bounding box.

        Returns:
            tuple: (offset, zoom)
        """

        min_point = CoordinatePoint(Coordinate(float("inf")), Coordinate(float("inf")))
        max_point = CoordinatePoint(Coordinate(float("-inf")), Coordinate(float("-inf")))
        
        for element in elements:
            bbox = element.get_bounding_box()
            if bbox is None:
                continue;
                
            self._BoundingBoxes.append(bbox)

            point1 = bbox[0]
            point2 = bbox[1]
            
            min_x = min(point1.x, point2.x)
            max_x = max(point1.x, point2.x)
            min_y = min(point1.y, point2.y)
            max_y = max(point1.y, point2.y)
            
            min_point.x = min(min_point.x, min_x)
            min_point.y = min(min_point.y, min_y)
            max_point.x = max(max_point.x, max_x)
            max_point.y = max(max_point.y, max_y)
        
        bbox_width = float(max_point.x - min_point.x) + margin * 2
        bbox_height = float(max_point.y - min_point.y) + margin * 2
                
        bbox_width = max(margin, bbox_width)
        bbox_height = max(margin, bbox_height) 
        
        zoom = min(target_width / bbox_width, target_height / bbox_height)
        
        offset_x = (target_width - bbox_width * zoom) / 2 - float(min_point.x) * zoom
        offset_y = (target_height - bbox_height * zoom) / 2 - float(min_point.y) * zoom
    
        offset_x += margin * zoom
        offset_y += margin * zoom
                
        return CoordinatePoint(Coordinate(offset_x), Coordinate(offset_y)), zoom

    
  
        