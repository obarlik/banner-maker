# effects/monochrome.py
# Monochrome effect generation

import numpy as np
from PIL import Image

def apply_monochrome(img):
    """Apply monochrome filter - black and white."""
    arr = np.array(img)
    
    # Convert to grayscale using luminance formula
    gray = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    
    # Apply to RGB channels
    arr[:, :, 0] = gray
    arr[:, :, 1] = gray
    arr[:, :, 2] = gray
    
    return Image.fromarray(arr, mode="RGBA")