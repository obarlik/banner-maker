# effects/vintage.py
# Vintage effect generation

import numpy as np
from PIL import Image
from .vignette import apply_vignette

def apply_vintage(img):
    """Apply vintage filter - sepia tone + vignette."""
    arr = np.array(img).astype(np.float32)
    
    # Sepia tone matrix
    sepia_matrix = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168], 
        [0.272, 0.534, 0.131]
    ])
    
    # Apply sepia to RGB channels
    if arr.shape[2] >= 3:
        rgb = arr[:, :, :3]
        sepia_rgb = np.dot(rgb, sepia_matrix.T)
        arr[:, :, :3] = np.clip(sepia_rgb, 0, 255)
    
    img_sepia = Image.fromarray(arr.astype(np.uint8), mode="RGBA")
    
    # Apply vignette
    return apply_vignette(img_sepia)