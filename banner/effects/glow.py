# effects/glow.py
# Glow effect generation

import numpy as np
from PIL import Image, ImageFilter
from ._utils import soft_light_blend

def apply_glow(img):
    """Apply overall glow effect - soft luminous appearance."""
    # Create glow version
    glow_img = img.filter(ImageFilter.GaussianBlur(radius=3))
    
    # Brighten the glow
    glow_arr = np.array(glow_img).astype(np.float32)
    glow_arr[:, :, :3] = np.clip(glow_arr[:, :, :3] * 1.3, 0, 255)
    glow_bright = Image.fromarray(glow_arr.astype(np.uint8), mode="RGBA")
    
    # Blend with original using soft light
    original_arr = np.array(img).astype(np.float32)
    glow_arr = np.array(glow_bright).astype(np.float32)
    
    result = soft_light_blend(original_arr, glow_arr)
    return Image.fromarray(result.astype(np.uint8), mode="RGBA")