# textures/leather.py
# Leather texture generation

import numpy as np
from PIL import Image
from ._utils import calculate_normal_map_from_heightmap, apply_lighting_to_image

def apply_leather(img, density=1.0, opacity=255, rotation=0, colors=None, SS=1, **kwargs):
    """Apply leather texture - organic bumps and grain."""
    img_array = np.array(img)
    h, w = img_array.shape[:2]
    
    # Leather has organic, random bumps
    grain_size = max(0.5, density)
    
    # Multi-scale leather grain
    coarse = np.random.normal(0, 0.1 * grain_size, (h//3, w//3))
    medium = np.random.normal(0, 0.05 * grain_size, (h//2, w//2))
    fine = np.random.normal(0, 0.02 * grain_size, (h, w))
    
    # Resize and combine
    from PIL import Image as PILImage
    coarse_img = PILImage.fromarray(((coarse + 0.2) * 255).astype(np.uint8), mode='L')
    coarse_full = np.array(coarse_img.resize((w, h), PILImage.BILINEAR)) / 255 - 0.2
    
    medium_img = PILImage.fromarray(((medium + 0.1) * 255).astype(np.uint8), mode='L')
    medium_full = np.array(medium_img.resize((w, h), PILImage.BILINEAR)) / 255 - 0.1
    
    heightmap = coarse_full * 0.6 + medium_full * 0.3 + fine * 0.1 + 0.1
    
    # Calculate normal map and apply lighting
    normal_map = calculate_normal_map_from_heightmap(heightmap, strength=8.0)
    lit_img = apply_lighting_to_image(img_array, normal_map, ambient=0.4)
    
    return Image.fromarray(lit_img, mode="RGBA")