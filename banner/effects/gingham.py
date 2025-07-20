# effects/gingham.py
# Gingham effect generation

import numpy as np
from PIL import Image
from ._utils import apply_contrast_adjustment, apply_color_tint

def apply_gingham(img):
    """Apply Gingham filter - neutral, clean, slight warm."""
    arr = np.array(img).astype(np.float32)
    
    # Neutral tone with slight warmth
    arr = apply_color_tint(arr, 1.05, 1.02, 0.98)
    
    # Slight contrast reduction for clean look
    arr[:, :, :3] = apply_contrast_adjustment(arr, 0.95)
    
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")