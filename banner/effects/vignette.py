# effects/vignette.py
# Vignette effect generation

import numpy as np
from PIL import Image
from ._utils import create_vignette_mask

def apply_vignette(img):
    """Apply vignette effect - darken edges."""
    arr = np.array(img)
    h, w = arr.shape[:2]
    
    # Create vignette mask
    vignette_mask = create_vignette_mask(h, w, strength=0.5)  # Stronger vignette
    
    # Apply vignette to RGB channels
    if arr.shape[2] == 4:  # RGBA
        arr[:, :, :3] = (arr[:, :, :3] * vignette_mask[..., np.newaxis]).astype(np.uint8)
    else:  # RGB
        arr = (arr * vignette_mask[..., np.newaxis]).astype(np.uint8)
    
    return Image.fromarray(arr, mode="RGBA")