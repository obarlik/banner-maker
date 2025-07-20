"""
Text (title, subtitle) processing
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from core.text_utils import get_text_width
from core.image_utils import get_outline_color, hex_to_rgb, get_contrast_color, contrast_ratio
import os

def find_font_path(font_name):
    # Add .ttf extension if not present
    if not os.path.splitext(font_name)[1]:
        font_name += ".ttf"
    # If no path specified, search in fonts/ directory first
    if not os.path.isabs(font_name) and not os.path.exists(font_name):
        font_path = os.path.join("fonts", font_name)
        if os.path.exists(font_path):
            return font_path
    return font_name

def add_text(img: Image.Image, config) -> Image.Image:
    """Adds title and subtitle."""
    title = getattr(config, 'title', 'Banner Maker')
    subtitle = getattr(config, 'subtitle', '')
    width = getattr(config, 'width', 1024)
    height = getattr(config, 'height', 256)
    SS = getattr(config, 'SuperSampling', 1)
    padding = getattr(config, 'padding', 32) * SS
    icon_position = getattr(config, 'icon_position', 'right')
    shadow = getattr(config, 'shadow', False)
    shadow_opacity = getattr(config, 'shadow_opacity', 100)
    title_font = getattr(config, 'title_font', 'fonts/Inter-Bold.ttf')
    subtitle_font = getattr(config, 'subtitle_font', 'fonts/Inter-Regular.ttf')
    text_color = getattr(config, 'text_color', None)
    min_contrast = getattr(config, 'min_contrast', 4.5)
    # New: text_box parameters
    text_box = getattr(config, 'text_box', False)
    text_box_color = getattr(config, 'text_box_color', 'rgba(0,0,0,0.35)')
    text_box_radius = getattr(config, 'text_box_radius', 8) * SS
    text_box_padding = getattr(config, 'text_box_padding', 12) * SS
    icon_size = int(height * 0.62)
    min_icon_margin = padding
    # Background colors (for outline and contrast)
    bg_color_start = getattr(config, 'bg_color_start', None)
    bg_color_end = getattr(config, 'bg_color_end', None)
    auto_color = getattr(config, 'auto_color', True)
    if auto_color and (not bg_color_start or not bg_color_end):
        bg_start = (60,60,60)
        bg_end = (200,200,200)
    else:
        bg_start = hex_to_rgb(bg_color_start) if isinstance(bg_color_start, str) else bg_color_start
        bg_end = hex_to_rgb(bg_color_end) if isinstance(bg_color_end, str) else bg_color_end
    avg_bg = tuple((a+b)//2 for a,b in zip(bg_start, bg_end)) if bg_start and bg_end else (128,128,128)
    # Text color contrast (improved, textbox-aware)
    if text_box and text_box_color == "auto":
        # First determine text color (if auto, based on background, otherwise from user)
        def luminance(rgb):
            r,g,b = [x/255.0 for x in rgb]
            return 0.299*r + 0.587*g + 0.114*b
        if text_color == "auto" or not text_color:
            lum_bg = luminance(avg_bg)
            if lum_bg > 0.45:
                text_rgb = (32,32,32)
            else:
                text_rgb = (255,255,255)
            if contrast_ratio(text_rgb, avg_bg) < min_contrast:
                white_contrast = contrast_ratio((255,255,255), avg_bg)
                black_contrast = contrast_ratio((32,32,32), avg_bg)
                text_rgb = (255,255,255) if white_contrast > black_contrast else (32,32,32)
        else:
            text_rgb = hex_to_rgb(text_color) if isinstance(text_color, str) else text_color
        # Now set box color to contrast with text color and be semi-transparent
        def get_contrast_box_color(rgb, bg_rgb, min_contrast=4.5):
            # rgb: text color
            # bg_rgb: background average
            # alpha: box opacity (0-255)
            lum = luminance(rgb)
            contrast = contrast_ratio(rgb, bg_rgb)
            if contrast < 5:
                alpha = 90  # 35% opacity
            elif contrast < 7:
                alpha = 64  # 25% opacity
            else:
                alpha = 38  # 15% opacity
            if lum > 0.5:
                return (0,0,0,alpha)  # Light text -> dark box
            else:
                return (255,255,255,alpha)  # Dark text -> light box
        box_color = get_contrast_box_color(text_rgb, avg_bg, min_contrast=min_contrast)
        # Auto text box color applied
    elif text_color == "auto" or not text_color:
        def luminance(rgb):
            r,g,b = [x/255.0 for x in rgb]
            return 0.299*r + 0.587*g + 0.114*b
        if text_box:
            # Convert RGBA string to tuple
            def parse_rgba(rgba_str):
                if isinstance(rgba_str, tuple):
                    if len(rgba_str) == 4 and isinstance(rgba_str[3], float) and rgba_str[3] <= 1:
                        return rgba_str[:3] + (int(rgba_str[3]*255),)
                    return rgba_str
                if isinstance(rgba_str, str) and rgba_str.startswith('rgba'):
                    vals = [float(v.strip()) for v in rgba_str[5:-1].split(',')]
                    r, g, b = [int(vals[i]) for i in range(3)]
                    a = int(vals[3]*255) if vals[3] <= 1 else int(vals[3])
                    return (r, g, b, a)
                if isinstance(rgba_str, str) and rgba_str.startswith('#'):
                    hex_color = rgba_str.lstrip('#')
                    if len(hex_color) == 8:
                        r = int(hex_color[0:2], 16)
                        g = int(hex_color[2:4], 16)
                        b = int(hex_color[4:6], 16)
                        a = int(hex_color[6:8], 16)
                        return (r, g, b, a)
                    elif len(hex_color) == 6:
                        return hex_to_rgb(rgba_str) + (180,)
                    else:
                        return hex_to_rgb(rgba_str) + (180,)
                return (0,0,0,90)
            box_color = parse_rgba(text_box_color)
            # Text box color parsed
            box_rgb = box_color[:3]
            lum = luminance(box_rgb)
            if lum > 0.45:
                text_rgb = (32,32,32)
            else:
                text_rgb = (255,255,255)
            # Ensure contrast
            if contrast_ratio(text_rgb, box_rgb) < min_contrast:
                white_contrast = contrast_ratio((255,255,255), box_rgb)
                black_contrast = contrast_ratio((32,32,32), box_rgb)
                text_rgb = (255,255,255) if white_contrast > black_contrast else (32,32,32)
        else:
            lum = luminance(avg_bg)
            if lum > 0.45:
                text_rgb = (32,32,32)
            else:
                text_rgb = (255,255,255)
            if contrast_ratio(text_rgb, avg_bg) < min_contrast:
                white_contrast = contrast_ratio((255,255,255), avg_bg)
                black_contrast = contrast_ratio((32,32,32), avg_bg)
                text_rgb = (255,255,255) if white_contrast > black_contrast else (32,32,32)
    else:
        text_rgb = hex_to_rgb(text_color) if isinstance(text_color, str) else text_color
    # Auto-adjust font size
    max_title_width = width - (icon_size + 3*min_icon_margin)
    max_block_height = int(height * 0.8)
    font_size = int(height * 0.25)
    max_title_chars = 22
    while font_size > 10*SS:
        try:
            font_title = ImageFont.truetype(find_font_path(title_font), font_size)
        except Exception as e:
            print(f"[WARN] Title font could not be loaded: {title_font} ({e}), using default font.")
            font_title = ImageFont.load_default()
            # If default font has no size info, assign manually
            if not hasattr(font_title, 'size'):
                font_title.size = font_size
        title_w = get_text_width(font_title, title)
        title_h = getattr(font_title, 'size', font_size)
        subtitle_font_size = max(10*SS, int(font_size * 0.45))
        try:
            font_subtitle = ImageFont.truetype(find_font_path(subtitle_font), subtitle_font_size)
        except Exception as e:
            print(f"[WARN] Subtitle font could not be loaded: {subtitle_font} ({e}), using default font.")
            font_subtitle = ImageFont.load_default()
            if not hasattr(font_subtitle, 'size'):
                font_subtitle.size = subtitle_font_size
        subtitle_w = get_text_width(font_subtitle, subtitle)
        subtitle_h = getattr(font_subtitle, 'size', subtitle_font_size)
        text_block_h = title_h + int(0.18*height) + subtitle_h
        if title_w < max_title_width and text_block_h < max_block_height and len(title) <= max_title_chars:
            break
        font_size -= 2*SS
    # Position calculations
    title_w, title_h = get_text_width(font_title, title), getattr(font_title, 'size', font_size)
    subtitle_w, subtitle_h = get_text_width(font_subtitle, subtitle), getattr(font_subtitle, 'size', subtitle_font_size)
    text_block_h = title_h + int(0.18*height) + subtitle_h
    icon_block_h = icon_size
    block_h = max(text_block_h, icon_block_h)
    block_y = (height - block_h) // 2
    if icon_position == "left":
        title_x = min_icon_margin + icon_size + min_icon_margin
    else:
        title_x = min_icon_margin
    title_y = block_y + (block_h - text_block_h)//2
    subtitle_y = title_y + title_h + int(0.18*height)
    draw = ImageDraw.Draw(img)
    outline_color = get_outline_color(text_rgb)
    # --- NEW: text_box drawing ---
    if text_box:
        # Calculate box size (for title + subtitle)
        box_left = title_x - text_box_padding
        box_top = title_y - text_box_padding
        box_right = max(title_x + title_w, title_x + subtitle_w) + text_box_padding
        box_bottom = subtitle_y + subtitle_h + text_box_padding
        # Convert RGBA string to tuple
        def parse_rgba(rgba_str):
            if isinstance(rgba_str, tuple):
                return rgba_str
            if rgba_str == "auto":
                return box_color if 'box_color' in locals() else (0,0,0,90)
            if rgba_str.startswith('rgba'):
                vals = rgba_str[5:-1].split(',')
                return tuple([int(float(v)) if i<3 else int(float(v)*255) if float(v)<=1 else int(float(v)) for i,v in enumerate(vals)])
            if rgba_str.startswith('#'):
                hex_color = rgba_str.lstrip('#')
                if len(hex_color) == 8:
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    a = int(hex_color[6:8], 16)
                    return (r, g, b, a)
                elif len(hex_color) == 6:
                    return hex_to_rgb(rgba_str) + (180,)
                else:
                    return hex_to_rgb(rgba_str) + (180,)
            return (0,0,0,90)
        box_color_draw = parse_rgba(text_box_color)
        # Text box background applied
        # Use overlay layer for transparent box
        overlay = Image.new("RGBA", img.size, (0,0,0,0))
        overlay_draw = ImageDraw.Draw(overlay)
        try:
            overlay_draw.rounded_rectangle([box_left, box_top, box_right, box_bottom], radius=text_box_radius, fill=box_color_draw)
        except:
            overlay_draw.rectangle([box_left, box_top, box_right, box_bottom], fill=box_color_draw)
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
    # ---
    # Shadow effect
    if shadow:
        shadow_layer = Image.new("RGBA", img.size, (0,0,0,0))
        shadow_draw = ImageDraw.Draw(shadow_layer)
        shadow_color = (0,0,0,shadow_opacity)
        shadow_offset = 4 * SS
        shadow_draw.text((title_x+shadow_offset, title_y+shadow_offset), title, font=font_title, fill=shadow_color)
        # Blur removed - SuperSampling provides anti-aliasing for shadows
        # shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=4*SS/2))
        img = Image.alpha_composite(img.convert("RGBA"), shadow_layer)
        draw = ImageDraw.Draw(img)
    # Outline
    for dx in [-2*SS,0,2*SS]:
        for dy in [-2*SS,0,2*SS]:
            if dx == 0 and dy == 0: continue
            draw.text((title_x+dx, title_y+dy), title, font=font_title, fill=outline_color)
    draw.text((title_x, title_y), title, font=font_title, fill=text_rgb)
    # Subtitle
    if shadow:
        shadow_layer = Image.new("RGBA", img.size, (0,0,0,0))
        shadow_draw = ImageDraw.Draw(shadow_layer)
        shadow_color = (0,0,0,shadow_opacity)
        shadow_offset = 2 * SS
        shadow_draw.text((title_x+shadow_offset, subtitle_y+shadow_offset), subtitle, font=font_subtitle, fill=shadow_color)
        # Blur removed - SuperSampling provides anti-aliasing for shadows
        # shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=3*SS/2))
        img = Image.alpha_composite(img.convert("RGBA"), shadow_layer)
        draw = ImageDraw.Draw(img)
    for dx in [-1*SS,0,1*SS]:
        for dy in [-1*SS,0,1*SS]:
            if dx == 0 and dy == 0: continue
            draw.text((title_x+dx, subtitle_y+dy), subtitle, font=font_subtitle, fill=outline_color)
    draw.text((title_x, subtitle_y), subtitle, font=font_subtitle, fill=text_rgb)
    return img 