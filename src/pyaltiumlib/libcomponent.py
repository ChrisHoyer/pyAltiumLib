import json

from pyaltiumlib.datatypes.coordinate import Coordinate, CoordinatePoint

class LibComponent:
    
    def __init__(self, parent, name, description):
        
        self.LibFile = parent
        self.Name = name
        self.Description = description
                    
        self.Records = [] 
        self._BoundingBoxes = []
        self.drawing_layer = {}
        
    
    def __repr__(self):
       symbol_data = {
           "Name": self.Name,
           "Description": self.Description
           }
        
       return json.dumps(symbol_data, indent=4)
   

# =============================================================================
#     Drawing related
# =============================================================================   
 
    
    def draw_svg(self, graphic, size_x, size_y, draw_bbox=False):
               
        validObj = []
        for obj in self.Records:
            if hasattr(obj, 'draw_svg') and callable(getattr(obj, 'draw_svg')):
                validObj.append( obj )
            else:
                print(f" object: {obj} has no drawing function")

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


    def _autoscale(self, elements, target_width, target_height, margin=10.0):
        """
        Adjusts the coordinates of elements to fit within the target dimensions using zoom.
        Args:
            elements (list): A list of objects with `get_BoundingBox` method.
            target_width (int): Target image width.
            target_height (int): Target image height.
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

    
  
        