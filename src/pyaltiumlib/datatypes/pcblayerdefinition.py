from pyaltiumlib.datatypes import ParameterColor

class PCBLayerDefinition:
    
    def __init__(self, id, name, drawing_order, color):
        
        self.id = id
        self.name = name
        self.svg_layer = name.replace(' ', '_')
        self.drawing_order = drawing_order
        self.color = ParameterColor(color)

    def __repr__(self):
        return f"{self.id}, {self.name}, {self.color.to_hex()}"        
    
    @classmethod
    def LoadDefaultLayers(cls):
        """
        Returns a list of default PCBLayerDefinition objects.
        """

        default_layers = [
            (0, "None", 0, 0),  
            (1, "Top Layer", 6, 255),
            (2, "Mid-Layer 1", 6, 93308),
            (3, "Mid-Layer 2", 6, 14738350),
            (4, "Mid-Layer 3", 6, 6737152),
            (5, "Mid-Layer 4", 6, 16737721),
            (6, "Mid-Layer 5", 6, 16776960),
            (7, "Mid-Layer 6", 6, 8388736),
            (8, "Mid-Layer 7", 6, 16711935),
            (9, "Mid-Layer 8", 6, 8421376),
            (10, "Mid-Layer 9", 6, 16777215),
            (11, "Mid-Layer 10", 6, 8421504),
            (12, "Mid-Layer 11", 6, 8388736),
            (13, "Mid-Layer 12", 6, 8421376),
            (14, "Mid-Layer 13", 6, 12632256),
            (15, "Mid-Layer 14", 6, 128),
            (16, "Mid-Layer 15", 6, 32768),
            (17, "Mid-Layer 16", 6, 65280),
            (18, "Mid-Layer 17", 6, 8388608),
            (19, "Mid-Layer 18", 6, 16776960),
            (20, "Mid-Layer 19", 6, 8388736),
            (21, "Mid-Layer 20", 6, 16711935),
            (22, "Mid-Layer 21", 6, 8421376),
            (23, "Mid-Layer 22", 6, 65535),
            (24, "Mid-Layer 23", 6, 8421504),
            (25, "Mid-Layer 24", 6, 16777215),
            (26, "Mid-Layer 25", 6, 8388736),
            (27, "Mid-Layer 26", 6, 8421376),
            (28, "Mid-Layer 27", 6, 12632256),
            (29, "Mid-Layer 28", 6, 128),
            (30, "Mid-Layer 29", 6, 32768),
            (31, "Mid-Layer 30", 6, 16711680),
            (32, "Bottom Layer", 6, 16711680),
            (33, "Top Overlay", 2, 65535),
            (34, "Bottom Overlay", 3, 8421376),
            (35, "Top Paste", 7, 8421504),
            (36, "Bottom Paste", 8, 128),
            (37, "Top Solder", 9, 8388736),
            (38, "Bottom Solder", 10, 16711935),
            (39, "Internal Plane 1", 11, 32768),
            (40, "Internal Plane 2", 11, 128),
            (41, "Internal Plane 3", 11, 8388736),
            (42, "Internal Plane 4", 11, 8421376),
            (43, "Internal Plane 5", 11, 32768),
            (44, "Internal Plane 6", 11, 128),
            (45, "Internal Plane 7", 11, 8388736),
            (46, "Internal Plane 8", 11, 8421376),
            (47, "Internal Plane 9", 11, 32768),
            (48, "Internal Plane 10", 11, 128),
            (49, "Internal Plane 11", 11, 8388736),
            (50, "Internal Plane 12", 11, 8421376),
            (51, "Internal Plane 13", 11, 32768),
            (52, "Internal Plane 14", 11, 128),
            (53, "Internal Plane 15", 11, 8388736),
            (54, "Internal Plane 16", 11, 8421376),
            (55, "Drill Guide", 12, 128),
            (56, "Keep-Out Layer", 13, 16711935),
            (57, "Mechanical 1", 14, 16711935),
            (58, "Mechanical 2", 14, 8388736),
            (59, "Mechanical 3", 14, 32768),
            (60, "Mechanical 4", 14, 8421376),
            (61, "Mechanical 5", 14, 16711935),
            (62, "Mechanical 6", 14, 8388736),
            (63, "Mechanical 7", 14, 32768),
            (64, "Mechanical 8", 14, 8421376),
            (65, "Mechanical 9", 14, 16711935),
            (66, "Mechanical 10", 14, 8388736),
            (67, "Mechanical 11", 14, 32768),
            (68, "Mechanical 12", 14, 8421376),
            (69, "Mechanical 13", 14, 16711935),
            (70, "Mechanical 14", 14, 8388736),
            (71, "Mechanical 15", 14, 32768),
            (72, "Mechanical 16", 14, 0),
            (73, "Drill Drawing", 15, 2944255),
            (74, "Multi-Layer", 1, 12632256),
            (75, "Connections", 4, 7695902),
            (76, "Background", 5, 0),
            (77, "DRC Error Markers", 0, 65280),
            (78, "Selections", 0, 16777215),
            (79, "Visible Grid 1", 101, 6045005),
            (80, "Visible Grid 2", 100, 9467537),
            (81, "Pad Holes", 1, 9473792),
            (82, "Via Holes", 1, 24961),
        ]


        return [cls(layer[0], layer[1], layer[2], layer[3]) for layer in default_layers]