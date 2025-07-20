# shapes/_utils.py
# Shared utilities for shape generation

from PIL import Image, ImageDraw
import math
import random

def create_shape_overlay(img):
    """Create a transparent overlay for shape drawing."""
    return Image.new("RGBA", img.size, (0,0,0,0))

def ensure_color_tuple(color):
    """Ensure color is a tuple."""
    if isinstance(color, list):
        return tuple(color)
    return color

def composite_shape(img, overlay):
    """Composite shape overlay onto image."""
    return Image.alpha_composite(img, overlay)

def calculate_default_center(W, H):
    """Calculate default center point."""
    return (W // 2, H // 2)

def calculate_default_radius(W, H, scale=0.35):
    """Calculate default radius based on dimensions."""
    return int(min(W, H) * scale)