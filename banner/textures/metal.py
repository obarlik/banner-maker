# textures/metal.py
# Metal texture generation

import numpy as np
from PIL import Image
from ._utils import calculate_normal_map_from_heightmap, apply_lighting_to_image

def apply_metal(img, density=1.0, opacity=255, rotation=0, colors=None, SS=1, **kwargs):
    """Apply brushed metal texture using height map."""
    img_array = np.array(img)
    h, w = img_array.shape[:2]
    
    # Generate brushed metal heightmap
    scratch_density = max(0.5, density)
    
    # Create directional scratches (horizontal brushing) - more pronounced, scale with SS
    heightmap = np.random.normal(0, 0.08 * scratch_density, (h, w))
    
    # Blur removed - SuperSampling provides anti-aliasing for brush direction
    heightmap_img = Image.fromarray(((heightmap + 0.2) * 255).astype(np.uint8), mode='L')
    heightmap = (np.array(heightmap_img).astype(np.float32) / 255) - 0.2
    
    # Calculate normal map and apply lighting - stronger metallic effect
    normal_map = calculate_normal_map_from_heightmap(heightmap, strength=12.0)
    lit_img = apply_lighting_to_image(img_array, normal_map, 
                                     light_dir=(-0.2, -0.9, 1.0), ambient=0.3)
    
    return Image.fromarray(lit_img, mode="RGBA")