# shapes/ellipse.py
# Ellipse shape generation

from PIL import Image, ImageDraw
from ._utils import create_shape_overlay, ensure_color_tuple, composite_shape

def apply_ellipse(img, W, H, SS, color=(120, 120, 255, 80), center=None, rx=None, ry=None, blur=24):
    blur = max(blur if blur is not None else 24, 0)
    
    overlay = create_shape_overlay(img)
    draw = ImageDraw.Draw(overlay)
    
    cx, cy = center if center else (W//2, H//2)
    rx = rx if rx else int(W*0.35)
    ry = ry if ry else int(H*0.35)
    bbox = [cx-rx, cy-ry, cx+rx, cy+ry]
    
    color = ensure_color_tuple(color)
    draw.ellipse(bbox, fill=color)
    
    return composite_shape(img, overlay)