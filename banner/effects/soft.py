# effects/soft.py
# Soft effect generation

import numpy as np
from PIL import Image, ImageFilter

def apply_soft(img):
    """Apply soft filter - gentle blur for dreamy effect."""
    # Light gaussian blur
    blurred = img.filter(ImageFilter.GaussianBlur(radius=2.0))  # Stronger blur
    
    # Blend with original (60% original, 40% blurred)
    arr_orig = np.array(img).astype(np.float32)
    arr_blur = np.array(blurred).astype(np.float32)
    
    result = arr_orig * 0.6 + arr_blur * 0.4  # More blur effect
    result = np.clip(result, 0, 255).astype(np.uint8)
    
    return Image.fromarray(result, mode="RGBA")