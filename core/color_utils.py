# color_utils.py
"""
Centralized color utilities for banner generation.
Consolidates all color-related functions from multiple modules.
"""

import random
from PIL import Image


def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple."""
    if isinstance(hex_color, tuple):
        return hex_color
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    if lv == 3:
        return tuple(int(hex_color[i]*2, 16) for i in range(3))
    elif lv == 6:
        return tuple(int(hex_color[i:i + 2], 16) for i in range(0, 6, 2))
    elif lv == 8:
        return tuple(int(hex_color[i:i + 2], 16) for i in range(0, 8, 2))
    return (0, 0, 0)


def rgb_to_hex(rgb):
    """Convert RGB tuple to hex string."""
    if isinstance(rgb, str):
        return rgb
    if len(rgb) >= 3:
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    return "#000000"

def parse_color(color, opacity=255):
    """
    Parse color from various formats (hex, tuple, rgba string) with opacity.
    Unified version from textures.py and motifs.py duplication.
    """
    if isinstance(color, str) and color.startswith("#"):
        try:
            hexstr = color.lstrip('#')
            if len(hexstr) == 3:
                hexstr = ''.join([c*2 for c in hexstr])
            if len(hexstr) == 6:
                return tuple(int(hexstr[i:i+2], 16) for i in (0, 2, 4)) + (opacity,)
            elif len(hexstr) == 8:
                return tuple(int(hexstr[i:i+2], 16) for i in (0, 2, 4, 6))
        except Exception:
            return (255, 255, 255, opacity)
    elif isinstance(color, tuple):
        if len(color) == 3:
            return color + (opacity,)
        elif len(color) == 4:
            # Use provided opacity or override with new one
            return color[:3] + (opacity,)
    # RGBA string support can be added here
    return (255, 255, 255, opacity)

def parse_color_to_hex(color):
    """Parse color and return hex string for legacy compatibility."""
    if isinstance(color, str) and color.startswith("#"):
        return color
    
    # Named color support
    color_names = {
        'red': '#ff0000',
        'green': '#00ff00',
        'blue': '#0000ff',
        'white': '#ffffff',
        'black': '#000000',
        'yellow': '#ffff00',
        'purple': '#800080',
        'orange': '#ffa500',
        'pink': '#ffc0cb',
        'gray': '#808080',
        'grey': '#808080',
        'navy': '#000080',
        'teal': '#008080',
        'lime': '#00ff00',
        'maroon': '#800000',
        'olive': '#808000',
        'silver': '#c0c0c0'
    }
    
    if isinstance(color, str) and color.lower() in color_names:
        return color_names[color.lower()]
    
    # Convert tuple to hex
    rgba = parse_color(color)
    return rgb_to_hex(rgba)
    
    return "#000000"


def parse_rgba_string(rgba_str):
    """Parse RGBA string like 'rgba(255,0,0,0.5)' to tuple."""
    if isinstance(rgba_str, tuple):
        if len(rgba_str) == 4 and isinstance(rgba_str[3], float) and rgba_str[3] <= 1:
            return rgba_str[:3] + (int(rgba_str[3] * 255),)
        return rgba_str
    if rgba_str == "auto":
        return None
    if rgba_str.startswith("rgba(") and rgba_str.endswith(")"):
        try:
            values = rgba_str[5:-1].split(',')
            r, g, b = map(int, values[:3])
            a = float(values[3]) if len(values) > 3 else 1.0
            return (r, g, b, int(a * 255))
        except:
            return (0, 0, 0, 89)
    return hex_to_rgb(rgba_str) + (255,)


def get_random_rotation(rotation):
    """Get random rotation value from range or return fixed value."""
    if isinstance(rotation, (list, tuple)) and len(rotation) == 2:
        return random.uniform(rotation[0], rotation[1])
    return rotation


def get_dominant_colors(image_path, n=2):
    """Extract dominant colors from image."""
    try:
        img = Image.open(image_path).convert('RGB').resize((64, 64))
        colors = img.getcolors(64*64)
        colors.sort(reverse=True)
        dominant = [c[1] for c in colors[:n]]
        while len(dominant) < n:
            dominant.append((0, 82, 204))
        return dominant
    except Exception:
        return [(0, 82, 204)] * n


def get_average_color(colors):
    """Calculate average color from list of RGB tuples."""
    if not colors:
        return (128, 128, 128)
    r = int(sum([c[0] for c in colors]) / len(colors))
    g = int(sum([c[1] for c in colors]) / len(colors))
    b = int(sum([c[2] for c in colors]) / len(colors))
    return (r, g, b)


def luminance(rgb):
    """Calculate relative luminance of RGB color."""
    def channel(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb[:3]  # Handle RGBA tuples
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(rgb1, rgb2):
    """Calculate contrast ratio between two colors."""
    l1 = luminance(rgb1)
    l2 = luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def get_contrast_color(rgb):
    """Get high contrast color (black or white) for given background."""
    yiq = ((rgb[0]*299)+(rgb[1]*587)+(rgb[2]*114))/1000
    return (0, 0, 0) if yiq >= 128 else (255, 255, 255)


def get_outline_color(rgb):
    """Get best outline color (black or white) based on contrast."""
    return (0, 0, 0) if contrast_ratio(rgb, (0, 0, 0)) > contrast_ratio(rgb, (255, 255, 255)) else (255, 255, 255)


def rgb_distance(c1, c2):
    """Calculate Euclidean distance between two RGB colors."""
    return ((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2) ** 0.5


def adjust_color(color, delta):
    """Adjust color brightness by delta value."""
    return tuple(max(0, min(255, x + delta)) for x in color[:3])


def interpolate_color(start, end, ratio):
    """Interpolate between two RGB colors."""
    return tuple(
        int(start[i] * (1 - ratio) + end[i] * ratio)
        for i in range(3)
    )


def get_random_colors(count=1):
    """Generate random RGB colors."""
    return [
        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for _ in range(count)
    ]


def validate_color(color):
    """Validate and normalize color tuple."""
    if isinstance(color, (list, tuple)) and len(color) >= 3:
        return tuple(max(0, min(255, int(c))) for c in color[:3])
    return (0, 0, 0)


def blend_colors(color1, color2, alpha=0.5):
    """Blend two colors with alpha blending."""
    return tuple(
        int(color1[i] * (1 - alpha) + color2[i] * alpha)
        for i in range(3)
    )