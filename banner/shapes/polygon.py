# shapes/polygon.py
# Polygon shape generation

from PIL import Image, ImageDraw
import math
from ._utils import create_shape_overlay, ensure_color_tuple, composite_shape

def apply_polygon(img, W, H, SS, color=(255, 80, 80, 80), center=None, radius=None, sides=6, rotation=0, blur=24):
    sides = max(sides if sides is not None else 6, 3)
    blur = max(blur if blur is not None else 24, 0)
    
    overlay = create_shape_overlay(img)
    draw = ImageDraw.Draw(overlay)
    
    cx, cy = center if center else (W//2, H//2)
    radius = radius if radius else int(min(W, H)*0.35)
    angle_offset = math.radians(rotation)
    
    points = [
        (
            int(cx + radius * math.cos(2*math.pi*i/sides + angle_offset)),
            int(cy + radius * math.sin(2*math.pi*i/sides + angle_offset))
        )
        for i in range(sides)
    ]
    
    color = ensure_color_tuple(color)
    draw.polygon(points, fill=color)
    
    return composite_shape(img, overlay)