# shapes/rectangle.py
# Rectangle shape generation

from PIL import Image, ImageDraw
from ._utils import create_shape_overlay, ensure_color_tuple, composite_shape

def apply_rectangle(img, W, H, SS, color=(100, 255, 100, 100), center=None, width=None, height=None, blur=0):
    """Create a rectangular shape."""
    color = ensure_color_tuple(color)
    
    overlay = create_shape_overlay(img)
    draw = ImageDraw.Draw(overlay)
    
    # Default center and dimensions
    if center is None:
        center = (W // 2, H // 2)
    if width is None:
        width = W // 3
    if height is None:
        height = H // 3
    
    # Calculate rectangle bounds
    left = center[0] - width // 2
    top = center[1] - height // 2
    right = center[0] + width // 2
    bottom = center[1] + height // 2
    
    draw.rectangle([left, top, right, bottom], fill=color)
    
    return composite_shape(img, overlay)