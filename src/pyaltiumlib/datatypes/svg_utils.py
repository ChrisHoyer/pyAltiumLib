import math

def get_arc_path(center, radius_x, radius_y, angle_start, angle_end):
    """
    Generate the SVG path data for the arc.

    Args:
        center (tuple): The center coordinates of the arc.
        radius_x (int): The x-radius of the arc.
        radius_y (int): The y-radius of the arc.

    Returns:
        str: The SVG path data for the arc.
    """
    def degrees_to_radians(degrees):
        return (degrees * math.pi / 180) % (2*math.pi)
    
    angle_start = degrees_to_radians(angle_start)
    angle_stop = degrees_to_radians(angle_end)
    
    if angle_start == angle_stop:
        angle_stop -= 0.001
    
    start_x = center[0] + radius_x * math.cos(-angle_start)
    start_y = center[1] + radius_y * math.sin(-angle_start)
    end_x = center[0] + radius_x * math.cos(-angle_stop)
    end_y = center[1] + radius_y * math.sin(-angle_stop)
    
    # Set large_arc_flag based on the angle difference
    large_arc_flag = 1 if (angle_stop - angle_start) % (2 * math.pi) > math.pi else 0
    
    # Set sweep_flag to 0 for counterclockwise
    sweep_flag = 0
    
    path_data = (
        f"M {start_x},{start_y} "
        f"A {radius_x},{radius_y} 0 {large_arc_flag},{sweep_flag} {end_x},{end_y}"
    )
    return path_data