# effects/matte.py
# Matte effect generation

import numpy as np
from PIL import Image
from ._utils import apply_saturation_boost

def apply_matte(img):
    """Apply matte filter - lifted blacks, film look."""
    arr = np.array(img).astype(np.float32)
    
    # Lift blacks (add slight brightness to dark areas)
    arr[:, :, :3] = arr[:, :, :3] * 0.9 + 25
    
    # Slight desaturation
    arr[:, :, :3] = apply_saturation_boost(arr, 0.8)
    
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")