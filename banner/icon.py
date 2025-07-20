"""
Icon processing
"""
from PIL import Image, ImageDraw, ImageFilter
from core.image_utils import get_average_color
import os

def add_icon(img: Image.Image, config) -> Image.Image:
    """
    Adds icon and applies necessary effects.
    """
    icon_path = getattr(config, 'icon_path', None)
    if not icon_path:
        if os.path.isfile("logo.png"):
            icon_path = "logo.png"
        elif os.path.isfile(os.path.join(os.path.dirname(__file__), "logo.png")):
            icon_path = os.path.join(os.path.dirname(__file__), "logo.png")
    width = getattr(config, 'width', 1024)
    height = getattr(config, 'height', 256)
    SS = getattr(config, 'SuperSampling', 1)
    padding = getattr(config, 'padding', 32) * SS
    icon_position = getattr(config, 'icon_position', 'right')
    icon_size = int(height * 0.62)
    min_icon_margin = padding
    bg_color_start = getattr(config, 'bg_color_start', None)
    bg_color_end = getattr(config, 'bg_color_end', None)
    auto_color = getattr(config, 'auto_color', True)
    # If background colors are automatic, they should be taken from config
    if auto_color and icon_path and (not bg_color_start or not bg_color_end):
        from core.image_utils import get_dominant_colors, hex_to_rgb
        dom_colors = get_dominant_colors(icon_path, 2)
        if not bg_color_start:
            bg_color_start = '#%02x%02x%02x' % dom_colors[0]
        if not bg_color_end:
            bg_color_end = '#%02x%02x%02x' % dom_colors[1]
    bg_start = bg_color_start
    bg_end = bg_color_end
    if isinstance(bg_start, str):
        from core.image_utils import hex_to_rgb
        bg_start = hex_to_rgb(bg_start)
    if isinstance(bg_end, str):
        from core.image_utils import hex_to_rgb
        bg_end = hex_to_rgb(bg_end)
    # Position calculations
    block_y = 0
    icon_block_h = icon_size
    block_h = icon_block_h
    block_y = (height - block_h) // 2
    if icon_position == "left":
        icon_x = min_icon_margin
        icon_y = block_y
    else:
        icon_x = width - icon_size - min_icon_margin
        icon_y = block_y
    # Icon processing
    if icon_path:
        try:
            icon = Image.open(icon_path).convert("RGBA")
            icon = icon.resize((icon_size, icon_size))
            # Logo glow/shadow (based on background color)
            avg_bg = get_average_color([bg_start, bg_end])
            if sum(avg_bg)<380:
                glow_color = (255,255,255,110)
            else:
                glow_color = (80,80,80,130)
            glow = Image.new("RGBA", (icon_size+40*SS, icon_size+40*SS), (0,0,0,0))
            glow_draw = ImageDraw.Draw(glow)
            glow_draw.ellipse([0,0,icon_size+40*SS,icon_size+40*SS], fill=glow_color)
            # Blur removed - SuperSampling provides anti-aliasing for glow
            # blur_glow = glow.filter(ImageFilter.GaussianBlur(radius=icon_size//7))
            # img.paste(blur_glow, (icon_x-20*SS, icon_y-20*SS), blur_glow)
            img.paste(glow, (icon_x-20*SS, icon_y-20*SS), glow)
            img.paste(icon, (icon_x, icon_y), icon)
        except Exception as e:
            print(f"[WARN] Icon could not be loaded: {e}")
    return img 