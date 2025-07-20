# effects/chromatic_aberration.py
# Chromatic aberration effect generation

import numpy as np
from PIL import Image

def apply_chromatic_aberration(img):
    """Apply chromatic aberration - RGB channel offset."""
    arr = np.array(img)
    h, w = arr.shape[:2]
    
    # Create offset channels
    result = arr.copy()
    
    # Shift red channel right
    if w > 2:
        result[:, 2:, 0] = arr[:, :-2, 0]
    
    # Shift blue channel left  
    if w > 2:
        result[:, :-2, 2] = arr[:, 2:, 2]
    
    return Image.fromarray(result, mode="RGBA")