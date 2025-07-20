# textures/concrete.py
# Concrete texture generation

import numpy as np
from PIL import Image
from ._utils import calculate_normal_map_from_heightmap, apply_lighting_to_image

def apply_concrete(img, density=1.0, opacity=255, rotation=0, colors=None, SS=1, **kwargs):
    """Apply concrete texture using multi-scale height map."""
    img_array = np.array(img)
    h, w = img_array.shape[:2]
    
    # Generate concrete heightmap with multiple scales
    scale_factor = max(0.5, density)
    
    # Coarse bumps - more dramatic
    coarse_scale = max(16, int(32 / scale_factor))
    coarse_h, coarse_w = h // 4, w // 4
    coarse = np.random.normal(0, 0.15, (coarse_h, coarse_w))
    
    # Resize coarse to full size
    from PIL import Image as PILImage
    coarse_img = PILImage.fromarray(((coarse + 0.3) * 255).astype(np.uint8), mode='L')
    coarse_resized = coarse_img.resize((w, h), PILImage.BILINEAR)
    coarse_full = (np.array(coarse_resized).astype(np.float32) / 255) - 0.3
    
    # Fine grain - stronger
    fine = np.random.normal(0, 0.08 * scale_factor, (h, w))
    
    # Combine scales
    heightmap = coarse_full * 0.8 + fine * 0.4
    
    # Calculate normal map and apply lighting - rougher concrete
    normal_map = calculate_normal_map_from_heightmap(heightmap, strength=10.0)
    lit_img = apply_lighting_to_image(img_array, normal_map, ambient=0.2)
    
    return Image.fromarray(lit_img, mode="RGBA")