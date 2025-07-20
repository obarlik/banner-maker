# textures/denim.py
# Denim texture generation

import numpy as np
from PIL import Image
from ._utils import calculate_normal_map_from_heightmap, apply_lighting_to_image

def apply_denim(img, density=1.0, opacity=255, rotation=0, colors=None, SS=1, **kwargs):
    """Apply denim texture - diagonal twill pattern."""
    img_array = np.array(img)
    h, w = img_array.shape[:2]
    
    # Denim has diagonal twill lines - scale with SS
    twill_spacing = max(3, int(8 * SS / density))
    
    x = np.arange(w)
    y = np.arange(h)
    X, Y = np.meshgrid(x, y)
    
    # Diagonal twill pattern
    diagonal = (X + Y) // twill_spacing
    twill_pattern = diagonal % 4  # 4-step twill repeat
    
    # Height based on twill step
    heightmap = twill_pattern / 4.0 * 0.2 + 0.1
    
    # Calculate normal map and apply lighting
    normal_map = calculate_normal_map_from_heightmap(heightmap, strength=12.0)
    lit_img = apply_lighting_to_image(img_array, normal_map, ambient=0.4)
    
    return Image.fromarray(lit_img, mode="RGBA")