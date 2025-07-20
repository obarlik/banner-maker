# effects/cool.py
# Cool effect generation

import numpy as np
from PIL import Image
from ._utils import apply_color_tint

def apply_cool(img):
    """Apply cool filter - blue tone shift."""
    arr = np.array(img).astype(np.float32)
    
    # Cool tone: reduce red, boost blue
    arr = apply_color_tint(arr, 0.8, 1.0, 1.2)  # Stronger cool effect
    
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")