# effects/_utils.py
# Shared utilities for effects generation

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import math

def apply_saturation_boost(arr, factor):
    """Apply saturation boost to RGB array."""
    rgb = arr[:, :, :3] / 255.0
    gray = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
    return (gray[..., np.newaxis] + (rgb - gray[..., np.newaxis]) * factor) * 255.0

def apply_contrast_adjustment(arr, factor):
    """Apply contrast adjustment to RGB array."""
    return ((arr[:, :, :3] / 255.0 - 0.5) * factor + 0.5) * 255.0

def apply_color_tint(arr, red_factor, green_factor, blue_factor):
    """Apply color tint to RGB array."""
    arr[:, :, 0] *= red_factor
    arr[:, :, 1] *= green_factor
    arr[:, :, 2] *= blue_factor
    return arr

def create_vignette_mask(h, w, strength=0.3):
    """Create a vignette mask."""
    y, x = np.ogrid[:h, :w]
    center_x, center_y = w // 2, h // 2
    
    # Distance from center
    distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    max_distance = np.sqrt(center_x**2 + center_y**2)
    
    # Vignette mask
    vignette_mask = 1.0 - (distance / max_distance) * strength
    return np.clip(vignette_mask, 1.0 - strength, 1.0)

def screen_blend(base, overlay, opacity=1.0):
    """Screen blend mode: result = 1 - (1-base)(1-overlay)"""
    result = 255 - (255 - base) * (255 - overlay * opacity) / 255
    return np.clip(result, 0, 255)

def soft_light_blend(base, overlay, opacity=0.3):
    """Soft light blend mode."""
    result = base + overlay * opacity
    return np.clip(result, 0, 255)