# effects/juno.py
# Juno effect generation

import numpy as np
from PIL import Image
from ._utils import apply_color_tint, apply_saturation_boost

def apply_juno(img):
    """Apply Juno filter - warm, vintage with lifted shadows."""
    arr = np.array(img).astype(np.float32)
    
    # Warm tone
    arr = apply_color_tint(arr, 1.15, 1.05, 0.85)
    
    # Lift shadows
    arr[:, :, :3] = arr[:, :, :3] * 0.85 + 30
    
    # Slight desaturation
    arr[:, :, :3] = apply_saturation_boost(arr, 0.9)
    
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")