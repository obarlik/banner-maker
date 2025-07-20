# effects/reyes.py
# Reyes effect generation

import numpy as np
from PIL import Image
from ._utils import apply_contrast_adjustment, apply_color_tint, apply_saturation_boost

def apply_reyes(img):
    """Apply Reyes filter - vintage, faded, lifted blacks."""
    arr = np.array(img).astype(np.float32)
    
    # Lift blacks significantly
    arr[:, :, :3] = arr[:, :, :3] * 0.8 + 40
    
    # Reduce contrast
    arr[:, :, :3] = apply_contrast_adjustment(arr, 0.8)
    
    # Warm, faded tone
    arr = apply_color_tint(arr, 1.1, 1.05, 0.9)
    
    # Desaturate
    arr[:, :, :3] = apply_saturation_boost(arr, 0.6)
    
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")