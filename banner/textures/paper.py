# textures/paper.py
# Paper texture generation

import numpy as np
from PIL import Image
from ._utils import calculate_normal_map_from_heightmap, apply_lighting_to_image

def apply_paper(img, density=1.0, opacity=255, rotation=0, colors=None, SS=1, **kwargs):
    """Apply paper fiber texture using height map."""
    img_array = np.array(img)
    h, w = img_array.shape[:2]
    
    # Generate paper fiber heightmap
    fiber_density = max(0.3, density)
    
    # Random fiber pattern - more visible
    heightmap = np.random.normal(0, 0.04 * fiber_density, (h, w))
    
    # Add some directional fibers - stronger
    direction_noise = np.random.normal(0, 0.02, (h//2, w))
    direction_img = Image.fromarray(((direction_noise + 0.1) * 255).astype(np.uint8), mode='L')
    direction_resized = direction_img.resize((w, h), Image.BILINEAR)
    direction_full = (np.array(direction_resized).astype(np.float32) / 255) - 0.1
    
    heightmap += direction_full * 0.5
    
    # Calculate normal map and apply lighting - more paper texture
    normal_map = calculate_normal_map_from_heightmap(heightmap, strength=6.0)
    lit_img = apply_lighting_to_image(img_array, normal_map, ambient=0.5)
    
    return Image.fromarray(lit_img, mode="RGBA")