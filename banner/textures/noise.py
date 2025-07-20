# textures/noise.py
# Noise texture generation

import numpy as np
from PIL import Image

def apply_noise(img, density=1.0, opacity=255, rotation=0, colors=None, SS=1, **kwargs):
    """Apply noise texture with configurable parameters."""
    arr = np.array(img)
    # Scale noise intensity by density (SS doesn't affect noise)
    noise_intensity = int(16 * density)
    noise = np.random.normal(0, noise_intensity, arr.shape).astype(np.int16)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")