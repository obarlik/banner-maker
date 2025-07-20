# effects/cyberpunk.py
# Cyberpunk effect generation

import numpy as np
from PIL import Image
from ._utils import apply_contrast_adjustment, apply_color_tint

def apply_cyberpunk(img):
    """Apply cyberpunk filter - neon cyan/magenta with high contrast."""
    arr = np.array(img).astype(np.float32)
    
    # High contrast
    arr[:, :, :3] = apply_contrast_adjustment(arr, 1.4)
    
    # Cyan/magenta color shift
    arr = apply_color_tint(arr, 1.2, 0.9, 1.3)
    
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")