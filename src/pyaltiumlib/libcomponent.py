from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint

import logging
from typing import List, Any, Dict

# Set up logging
logger = logging.getLogger(__name__)

class LibComponent:
    """
    Base class represent a basic component Altium Designer library files.

    This class provides fundamental functionality for reading and illustrating
    Altium Designer components
    
    :param class parent: reference to library file :class:`pyaltiumlib.schlib.lib.SchLib` or :class:`pyaltiumlib.pcblib.lib.PcbLib`
    :param string name: name of the component
    :param string description: description of the component
    """

    LibFile = None
    """
    `class` that references to library file
    """

    Name = ''
    """`string` that contains the name of the component
    """

    Description = ''
    """
    `string` that contains the description of the component
    """

    Records = []
    """
    `List[any]` is a collection of records in their specific class 
    contained in the library.
    """
    
    def __init__(self, parent, name: str, description: str):
        """
        Initialize a LibComponent object.

        """        
        self.LibFile = parent
        self.Name = name
        self.Description = description                  
        self.Records = []
        
        self._BoundingBoxes = []
        self._graphic_layers = {}
       

    def __repr__(self) -> Dict:
        """
        Converts name and descirption to a dictionary.

        :return: A dict representation of the object
        :rtype: Dict
        """
        return self.read_meta()


    def read_meta(self) -> Dict:
        """
        Converts name and descirption to a dictionary.

        :return: A dict representation of the object
        :rtype: Dict
        """
        component_data = {
           "Name": self.Name,
           "Description": self.Description
           }
        return component_data 
       

# =============================================================================
#     Drawing related
# =============================================================================   
 
    
    def draw_svg(self, graphic, size_x: float, size_y: float, draw_bbox: bool = False) -> None:
        """
        Draw all drawable records the component to an svg drawing. All records are
        autoscaled to fit the given drawing object size.

        :param svgwrite.Drawing graphic: the svgwrite drawing object
        :param float size_x: The width of the svgwrite drawing object
        :param float size_y: The height of the svgwrite drawing object        
        :param bool [optional] draw_bbox: Draw bounding boxes
            
        :raises ImportError: If 'svgwrite' module is not installed.
        :raises ValueError: If 'graphic' is not the right instance.
        """    
        
        try:
            import svgwrite
        except ImportError:
            logger.error("The 'svgwrite' module is not installed. Install it using 'pip install svgwrite'.")

        if not isinstance(graphic, svgwrite.Drawing):
            logger.error("The provided 'dwg' object is not an instance of 'svgwrite.Drawing'.")

        
        validObj = []
        for obj in self.Records:
            if hasattr(obj, 'draw_svg') and callable(getattr(obj, 'draw_svg')):
                if obj.is_initialized:
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
        self._graphic_layers = {}
        if hasattr(self, 'LibFile'):
            if hasattr(self.LibFile, 'Layers'):
                for x in sorted(self.LibFile.Layers, key=lambda obj: obj.drawing_order, reverse=True):
                    self._graphic_layers[x.id] = graphic.add(graphic.g(id=x.svg_layer))
                                
        if draw_bbox:
            for obj in validObj:
                    obj.draw_bounding_box( graphic, offset, zoom)
            
        # Draw Primitives
        for obj in validObj:
            obj.draw_svg( graphic, offset, zoom)
          


    def _autoscale(self, elements: List[Any], target_width: float, target_height: float, margin: float = 10.0) -> tuple:
        """
        Adjust the coordinates of elements to fit within the target dimensions using zoom.
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

    
  
        