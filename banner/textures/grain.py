# textures/grain.py
# Grain texture generation

import numpy as np
from PIL import Image

def apply_grain(img, density=1.0, opacity=255, rotation=0, colors=None, SS=1, **kwargs):
    """Apply grain texture with configurable parameters.""" 
    arr = np.array(img)
    # Scale grain intensity by density (SS doesn't affect grain)
    grain_intensity = int(10 * density)
    noise = np.random.normal(0, grain_intensity, arr.shape).astype(np.int16)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")