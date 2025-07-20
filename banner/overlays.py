# overlays.py
# Functions for banner overlay effects
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math

def overlay_simple(img, W, H, SS):
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.polygon([
        (0, H//3), (W, 0), (W, H//3), (0, H)
    ], fill=(255,255,255,60))
    # Blur removed - SuperSampling provides anti-aliasing
    # overlay = overlay.filter(ImageFilter.GaussianBlur(radius=16*SS))
    return Image.alpha_composite(img, overlay)

def overlay_color(img, W, H, SS, color=(0,0,0,80), blur=0):
    overlay = Image.new("RGBA", img.size, color)
    # Blur removed - SuperSampling provides anti-aliasing
    # if blur > 0:
    #     overlay = overlay.filter(ImageFilter.GaussianBlur(radius=blur*SS))
    return Image.alpha_composite(img, overlay)

def overlay_gradient(img, W, H, SS, color1=(0,0,0,80), color2=(255,255,255,0), direction="vertical", blur=0):
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    arr = np.zeros((H, W, 4), dtype=np.uint8)
    if direction == "vertical":
        for y in range(H):
            alpha = y / (H-1)
            c = [int(color1[i]*(1-alpha) + color2[i]*alpha) for i in range(4)]
            arr[y, :, :] = c
    elif direction == "horizontal":
        for x in range(W):
            alpha = x / (W-1)
            c = [int(color1[i]*(1-alpha) + color2[i]*alpha) for i in range(4)]
            arr[:, x, :] = c
    elif direction == "diagonal":
        for y in range(H):
            for x in range(W):
                alpha = ((x+y) / (W+H-2))
                c = [int(color1[i]*(1-alpha) + color2[i]*alpha) for i in range(4)]
                arr[y, x, :] = c
    overlay = Image.fromarray(arr, mode="RGBA")
    # Blur removed - SuperSampling provides anti-aliasing
    # if blur > 0:
    #     overlay = overlay.filter(ImageFilter.GaussianBlur(radius=blur*SS))
    return Image.alpha_composite(img, overlay)

def overlay_lens_flare(img, W, H, SS, center=None):
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = center if center else (int(W*0.7), int(H*0.3))
    
    # Simple, subtle lens flare - just a gentle glow
    base_radius = int(40 * SS)  # SS scaled radius
    
    # Main subtle glow
    draw.ellipse([cx-base_radius, cy-base_radius, cx+base_radius, cy+base_radius], 
                 fill=(255,255,255,30))
    
    # Smaller inner glow
    inner_radius = int(20 * SS)  # SS scaled inner radius
    draw.ellipse([cx-inner_radius, cy-inner_radius, cx+inner_radius, cy+inner_radius], 
                 fill=(255,255,255,40))
    
    return Image.alpha_composite(img, overlay)

# Extensible overlay function map
OVERLAY_MAP = {
    "simple": overlay_simple,
    "color": overlay_color,
    "gradient": overlay_gradient,
    "lens_flare": overlay_lens_flare,
}