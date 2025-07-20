# effects/valencia.py
# Valencia effect generation

import numpy as np
from PIL import Image
from ._utils import apply_contrast_adjustment, apply_color_tint

def apply_valencia(img):
    """Apply Valencia filter - warm, dreamy, soft contrast."""
    arr = np.array(img).astype(np.float32)
    
    # Warm orange tone
    arr = apply_color_tint(arr, 1.2, 1.1, 0.8)
    
    # Soft contrast
    arr[:, :, :3] = apply_contrast_adjustment(arr, 0.9)
    
    # Lift shadows slightly
    arr[:, :, :3] = arr[:, :, :3] * 0.95 + 15
    
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")