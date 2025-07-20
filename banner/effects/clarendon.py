# effects/clarendon.py
# Clarendon effect generation

import numpy as np
from PIL import Image
from ._utils import apply_contrast_adjustment, apply_saturation_boost

def apply_clarendon(img):
    """Apply Clarendon filter - bright highlights, dark shadows."""
    arr = np.array(img).astype(np.float32)
    
    # High contrast curve
    arr[:, :, :3] = apply_contrast_adjustment(arr, 1.5)
    
    # Boost saturation
    arr[:, :, :3] = apply_saturation_boost(arr, 1.3)
    
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")