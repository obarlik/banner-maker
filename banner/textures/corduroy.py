# textures/corduroy.py
# Corduroy texture generation

import numpy as np
from PIL import Image
from ._utils import calculate_normal_map_from_heightmap, apply_lighting_to_image

def apply_corduroy(img, density=1.0, opacity=255, rotation=0, colors=None, SS=1, **kwargs):
    """Apply corduroy texture - vertical ribs/channels."""
    img_array = np.array(img)
    h, w = img_array.shape[:2]
    
    # Corduroy has vertical ribs - scale with SS
    rib_width = max(2, int(8 * SS / density))
    
    x = np.arange(w)
    X = np.tile(x, (h, 1))
    
    # Vertical rib pattern
    rib_position = X // rib_width
    rib_pattern = rib_position % 2
    
    # Raised ribs vs valleys
    heightmap = np.where(rib_pattern, 0.4, 0.0) + 0.1
    
    # Calculate normal map and apply lighting
    normal_map = calculate_normal_map_from_heightmap(heightmap, strength=20.0)
    lit_img = apply_lighting_to_image(img_array, normal_map, ambient=0.2)
    
    return Image.fromarray(lit_img, mode="RGBA")