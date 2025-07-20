# effects/lark.py
# Lark effect generation

import numpy as np
from PIL import Image
from ._utils import apply_saturation_boost, apply_color_tint

def apply_lark(img):
    """Apply Lark filter - bright, airy, desaturated."""
    arr = np.array(img).astype(np.float32)
    
    # Brighten overall
    arr[:, :, :3] += 20
    
    # Desaturate
    arr[:, :, :3] = apply_saturation_boost(arr, 0.7)
    
    # Cool tone
    arr = apply_color_tint(arr, 0.95, 1.0, 1.05)
    
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")