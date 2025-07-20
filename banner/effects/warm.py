# effects/warm.py
# Warm effect generation

import numpy as np
from PIL import Image
from ._utils import apply_color_tint

def apply_warm(img):
    """Apply warm filter - orange/yellow tone shift."""
    arr = np.array(img).astype(np.float32)
    
    # Warm tone: boost red/yellow, reduce blue
    arr = apply_color_tint(arr, 1.2, 1.1, 0.8)  # Stronger warm effect
    
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")