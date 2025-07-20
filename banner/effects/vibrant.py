# effects/vibrant.py
# Vibrant effect generation

import numpy as np
from PIL import Image
from ._utils import apply_saturation_boost, apply_contrast_adjustment

def apply_vibrant(img):
    """Apply vibrant filter - boost saturation and slight contrast."""
    arr = np.array(img).astype(np.float32)
    
    # Boost saturation
    arr[:, :, :3] = apply_saturation_boost(arr, 1.5)
    
    # Slight contrast boost
    arr[:, :, :3] = apply_contrast_adjustment(arr, 1.1)
    
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")