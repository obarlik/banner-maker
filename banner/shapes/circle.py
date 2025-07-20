# shapes/circle.py
# Circle shape generation

from PIL import Image, ImageDraw
from ._utils import create_shape_overlay, ensure_color_tuple, composite_shape

def apply_circle(img, W, H, SS, color=(255, 100, 100, 100), center=None, radius=None, blur=0):
    """Create a circular shape."""
    color = ensure_color_tuple(color)
    
    overlay = create_shape_overlay(img)
    draw = ImageDraw.Draw(overlay)
    
    # Default center and radius
    if center is None:
        center = (W // 2, H // 2)
    if radius is None:
        radius = min(W, H) // 4
    
    # Draw circle
    left = center[0] - radius
    top = center[1] - radius
    right = center[0] + radius
    bottom = center[1] + radius
    
    draw.ellipse([left, top, right, bottom], fill=color)
    
    return composite_shape(img, overlay)