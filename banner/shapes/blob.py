# shapes/blob.py
# Blob shape generation

from PIL import Image, ImageDraw
import math
import random
from ._utils import create_shape_overlay, ensure_color_tuple, composite_shape

def apply_blob(img, W, H, SS, color=(255, 140, 0, 90), seed=42, scale=0.7, blur=24):
    scale = max(scale if scale is not None else 0.7, 0.05)
    blur = max(blur if blur is not None else 24, 0)
    random.seed(seed)
    
    overlay = create_shape_overlay(img)
    draw = ImageDraw.Draw(overlay)
    
    # Simple blob algorithm: random points around center
    cx, cy = int(W*0.5), int(H*0.5)
    r = int(min(W, H) * scale * 0.5)
    points = []
    n = 8
    
    for i in range(n):
        angle = 2 * math.pi * i / n
        radius = r * (0.85 + 0.3 * random.random())
        x = int(cx + radius * math.cos(angle))
        y = int(cy + radius * math.sin(angle))
        points.append((x, y))
    
    color = ensure_color_tuple(color)
    draw.polygon(points, fill=color)
    
    return composite_shape(img, overlay)