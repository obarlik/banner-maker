# shapes/triangle.py
# Triangle shape generation

from PIL import Image, ImageDraw
from ._utils import create_shape_overlay, ensure_color_tuple, composite_shape

def apply_triangle(img, W, H, SS, color=(100, 100, 255, 100), center=None, size=None, blur=0):
    """Create a triangular shape."""
    color = ensure_color_tuple(color)
    
    overlay = create_shape_overlay(img)
    draw = ImageDraw.Draw(overlay)
    
    # Default center and size
    if center is None:
        center = (W // 2, H // 2)
    if size is None:
        size = min(W, H) // 4
    
    # Calculate triangle points (equilateral triangle)
    cx, cy = center
    height = int(size * 0.866)  # Height of equilateral triangle
    
    # Top point
    top = (cx, cy - height // 2)
    # Bottom left point
    bottom_left = (cx - size // 2, cy + height // 2)
    # Bottom right point
    bottom_right = (cx + size // 2, cy + height // 2)
    
    points = [top, bottom_left, bottom_right]
    draw.polygon(points, fill=color)
    
    return composite_shape(img, overlay)