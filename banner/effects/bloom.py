# effects/bloom.py
# Bloom effect generation

import numpy as np
from PIL import Image, ImageFilter

def apply_bloom(img):
    """Apply bloom effect - brightness-based gradient bloom."""
    arr = np.array(img).astype(np.float32)
    
    # Calculate brightness (luminance) for each pixel
    brightness = (arr[:, :, 0] * 0.299 + arr[:, :, 1] * 0.587 + arr[:, :, 2] * 0.114)
    
    # Create gradient bloom strength based on brightness
    # White (255) = full bloom, darker colors = less bloom
    bloom_strength = np.zeros_like(brightness)
    
    # Gradient bloom: starts at 160, full at 220+ (lowered thresholds)
    mask_medium = brightness >= 160
    mask_bright = brightness >= 220
    
    # Medium brightness: gradual bloom increase
    bloom_strength[mask_medium] = (brightness[mask_medium] - 160) / (220 - 160)
    # High brightness: full bloom
    bloom_strength[mask_bright] = 1.0
    
    # Apply bloom strength to each color channel
    bloom_arr = np.zeros_like(arr)
    for i in range(3):  # RGB channels
        bloom_arr[:, :, i] = arr[:, :, i] * bloom_strength
    
    # Alpha channel stays original
    bloom_arr[:, :, 3] = arr[:, :, 3]
    
    # Convert to PIL and blur
    bloom_layer = Image.fromarray(bloom_arr.astype(np.uint8), mode="RGBA")
    bloom_blurred = bloom_layer.filter(ImageFilter.GaussianBlur(radius=8))
    
    # Blend with original (screen blend mode)
    bloom_arr = np.array(bloom_blurred).astype(np.float32)
    
    # Slightly stronger screen blend
    result = 255 - (255 - arr) * (255 - bloom_arr * 0.8) / 255
    result = np.clip(result, 0, 255).astype(np.uint8)
    
    return Image.fromarray(result, mode="RGBA")