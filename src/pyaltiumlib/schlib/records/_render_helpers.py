import numpy as np
import math

def generate_bezier_points(vertices, num_points=100):
    """
    Generate points along a Bézier curve using De Casteljau's algorithm.
    Args:
        vertices (list): List of control points [(x1, y1), (x2, y2), ...].
        num_points (int): Number of points to generate along the curve.
    Returns:
        list: List of points [(x, y), ...] representing the Bézier curve.
    """
    def de_casteljau(control_points, t):
        """
        Perform De Casteljau's algorithm to compute a point on the Bézier curve.
        Args:
            control_points (list): List of control points.
            t (float): Parameter (0 <= t <= 1).
        Returns:
            tuple: A point (x, y) on the Bézier curve.
        """
        while len(control_points) > 1:
            control_points = [
                (
                    (1 - t) * p1[0] + t * p2[0],
                    (1 - t) * p1[1] + t * p2[1]
                )
                for p1, p2 in zip(control_points[:-1], control_points[1:])
            ]
        return control_points[0]
    

    return [ de_casteljau(vertices, t) for t in np.linspace(0, 1, num_points)]


def draw_dashed_line(graphic, start, end, color, width, dash_length=10, gap_length=10):
    """
    Draw a dashed line between two points.
    """

    total_distance = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    if total_distance == 0:
        return
    
    direction = ((end[0] - start[0]) / total_distance, (end[1] - start[1]) / total_distance)
    
    current_distance = 0
    current_pos = start
    
    while current_distance < total_distance:
        dash_end = (
            current_pos[0] + direction[0] * dash_length,
            current_pos[1] + direction[1] * dash_length
        )
        

        if math.sqrt((dash_end[0] - start[0])**2 + (dash_end[1] - start[1])**2) > total_distance:
            dash_end = end
        
        graphic.line([current_pos, dash_end], fill=color, width=width)
        
        current_distance += dash_length + gap_length
        current_pos = (
            current_pos[0] + direction[0] * (dash_length + gap_length),
            current_pos[1] + direction[1] * (dash_length + gap_length)
        )
