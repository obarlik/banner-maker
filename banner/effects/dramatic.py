# effects/dramatic.py
# Dramatic effect generation

import numpy as np
from PIL import Image
from ._utils import apply_contrast_adjustment, apply_saturation_boost

def apply_dramatic(img):
    """Apply dramatic filter - high contrast and saturation."""
    arr = np.array(img).astype(np.float32)
    
    # Increase contrast
    arr[:, :, :3] = apply_contrast_adjustment(arr, 1.3)
    
    # Increase saturation
    arr[:, :, :3] = apply_saturation_boost(arr, 1.2)
    
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")