# textures/canvas.py
# Canvas texture generation

import numpy as np
from PIL import Image
from ._utils import calculate_normal_map_from_heightmap, apply_lighting_to_image

def apply_canvas(img, density=1.0, opacity=255, rotation=0, colors=None, SS=1, **kwargs):
    """Apply canvas texture - classic square weave pattern."""
    img_array = np.array(img)
    h, w = img_array.shape[:2]
    
    # Canvas has simple, regular square weave - scale with SS
    thread_size = max(4, int(12 * SS / density))
    
    x = np.arange(w)
    y = np.arange(h)
    X, Y = np.meshgrid(x, y)
    
    # Simple checkerboard pattern for over/under
    pattern_x = (X // thread_size) % 2
    pattern_y = (Y // thread_size) % 2
    checkerboard = pattern_x ^ pattern_y
    
    # Height variation
    heightmap = np.where(checkerboard, 0.3, 0.1)
    
    # Calculate normal map and apply lighting
    normal_map = calculate_normal_map_from_heightmap(heightmap, strength=15.0)
    lit_img = apply_lighting_to_image(img_array, normal_map, ambient=0.3)
    
    return Image.fromarray(lit_img, mode="RGBA")