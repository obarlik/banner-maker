# shapes/diagonal_bar.py
# Diagonal bar shape generation

from PIL import Image, ImageDraw
from math import radians, tan
from ._utils import create_shape_overlay, ensure_color_tuple, composite_shape

def apply_diagonal_bar(img, W, H, SS, color=(0, 0, 0, 60), angle=30, thickness=0.25, blur=16):
    angle = angle if angle is not None else 30
    thickness = max(thickness if thickness is not None else 0.25, 0.01)
    blur = max(blur if blur is not None else 16, 0)
    
    overlay = create_shape_overlay(img)
    draw = ImageDraw.Draw(overlay)
    
    # Bar width
    bar_w = int(H * thickness)
    # Calculate bar corner points (top-left to bottom-right)
    offset = int(bar_w / tan(radians(angle))) if angle != 0 else 0
    points = [
        (0, 0),
        (W, 0),
        (W - offset, bar_w),
        (offset, bar_w)
    ]
    
    color = ensure_color_tuple(color)
    draw.polygon(points, fill=color)
    
    return composite_shape(img, overlay)