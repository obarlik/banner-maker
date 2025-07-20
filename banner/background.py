"""
Background and texture processing
"""
from PIL import Image, ImageDraw
from banner.textures import TEXTURE_MAP
from banner.patterns import PATTERN_MAP
from core.image_utils import hex_to_rgb, get_dominant_colors, get_average_color, rgb_distance, adjust_color, draw_gradient_custom
import os
import numpy as np

def draw_asym_rounded_rectangle(draw, box, radii, fill=None, outline=None, width=1, SS=1):
    x0, y0, x1, y1 = box
    tl, tr, br, bl = radii
    # Fill first if fill is provided
    if fill is not None:
        x_left = x0 + max(tl, bl)
        x_right = x1 - max(tr, br)
        y_top = y0 + max(tl, tr)
        y_bottom = y1 - max(bl, br)
        if x_left > x_right:
            x_left = x_right = (x_left + x_right) // 2
        if y_top > y_bottom:
            y_top = y_bottom = (y_top + y_bottom) // 2
        draw.pieslice([x0, y0, x0+2*tl, y0+2*tl], 180, 270, fill=fill)
        draw.pieslice([x1-2*tr, y0, x1, y0+2*tr], 270, 360, fill=fill)
        draw.pieslice([x1-2*br, y1-2*br, x1, y1], 0, 90, fill=fill)
        draw.pieslice([x0, y1-2*bl, x0+2*bl, y1], 90, 180, fill=fill)
        def safe_rect(a, b, c, d):
            x0_, x1_ = sorted([a, c])
            y0_, y1_ = sorted([b, d])
            if x0_ < x1_ and y0_ < y1_:
                draw.rectangle([x0_, y0_, x1_, y1_], fill=fill)
        safe_rect(x0+tl, y0, x1-tr, y0+max(tl,tr))
        safe_rect(x0, y0+tl, x0+max(tl,bl), y1-bl)
        safe_rect(x1-max(tr,br), y0+tr, x1, y1-br)
        safe_rect(x0+bl, y1-max(bl,br), x1-br, y1)
        safe_rect(x_left, y_top, x_right, y_bottom)
    # Outline (border) drawing
    if outline is not None and width > 0:
        # Fill outer shape with border color
        draw_asym_rounded_rectangle(draw, box, radii, fill=outline, SS=SS)
        # Fill inner shape (shrunk by border_width) with transparent
        shrink = width * SS
        inner_box = [x0+shrink, y0+shrink, x1-shrink, y1-shrink]
        inner_radii = [max(0, r-shrink) for r in radii]
        draw_asym_rounded_rectangle(draw, inner_box, inner_radii, fill=(0,0,0,0), SS=SS)

# Import BannerConfig if needed

def create_background(config) -> Image.Image:
    """Creates background, gradient and texture."""
    # Color and size settings
    auto_color = getattr(config, 'auto_color', True)
    icon_path = getattr(config, 'icon_path', None)
    bg_color_start = getattr(config, 'bg_color_start', "#0052CC") or "#0052CC"
    bg_color_end = getattr(config, 'bg_color_end', "#172B4D") or "#172B4D"
    text_color = getattr(config, 'text_color', "#FFFFFF") or "#FFFFFF"
    width = getattr(config, 'width', 1024)
    height = getattr(config, 'height', 256)
    SS = getattr(config, 'SuperSampling', 1)
    gradient_type = getattr(config, 'gradient_type', 'vertical')
    texture = getattr(config, 'texture', 'none')
    texture_density = getattr(config, 'texture_density', 1.0)
    texture_opacity = getattr(config, 'texture_opacity', 20)
    border = getattr(config, 'border', False)
    rounded = getattr(config, 'rounded', False)
    corner_radius_tl = getattr(config, 'corner_radius_tl', None)
    corner_radius_tr = getattr(config, 'corner_radius_tr', None)
    corner_radius_bl = getattr(config, 'corner_radius_bl', None)
    corner_radius_br = getattr(config, 'corner_radius_br', None)
    padding = getattr(config, 'padding', 32) * SS

    # Automatic color selection
    if auto_color and icon_path and (not bg_color_start or not bg_color_end):
        dom_colors = get_dominant_colors(icon_path, 2)
        if not bg_color_start:
            bg_color_start = '#%02x%02x%02x' % dom_colors[0]
        if not bg_color_end:
            bg_color_end = '#%02x%02x%02x' % dom_colors[1]
    bg_start = hex_to_rgb(bg_color_start) if isinstance(bg_color_start, str) else bg_color_start
    bg_end = hex_to_rgb(bg_color_end) if isinstance(bg_color_end, str) else bg_color_end
    # Gradient difference check (skip in test mode)
    test_mode = getattr(config, 'test_mode', False)
    if not test_mode:
        min_grad_dist = 40
        if rgb_distance(bg_start, bg_end) < min_grad_dist:
            if sum(bg_end) > sum(bg_start):
                bg_end = adjust_color(bg_end, 60)
            else:
                bg_end = adjust_color(bg_end, -60)
    border_radius = (height // 6 if rounded else 0) * SS
    border_width = (4 if border else 0) * SS
    mask_box = [0, 0, width-1, height-1]
    if border:
        inner_box = [border_width, border_width, width-border_width-1, height-border_width-1]
        bg_box = [border_width, border_width, width-border_width-1, height-border_width-1]
    else:
        inner_box = mask_box
        bg_box = mask_box
    corners = [corner_radius_tl, corner_radius_tr, corner_radius_br, corner_radius_bl]
    img = Image.new("RGBA", (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    if any(c is not None for c in corners):
        cr_tl = corner_radius_tl if corner_radius_tl is not None else border_radius
        cr_tr = corner_radius_tr if corner_radius_tr is not None else border_radius
        cr_br = corner_radius_br if corner_radius_br is not None else border_radius
        cr_bl = corner_radius_bl if corner_radius_bl is not None else border_radius
        if border:
            draw_asym_rounded_rectangle(draw, mask_box, (cr_tl, cr_tr, cr_br, cr_bl), fill=(200,200,200,255), SS=SS)
            draw_asym_rounded_rectangle(draw, inner_box, (max(0,cr_tl-border_width), max(0,cr_tr-border_width), max(0,cr_br-border_width), max(0,cr_bl-border_width)), fill=(0,0,0,0), SS=SS)
        grad = Image.new("RGBA", (width, height), (0,0,0,0))
        draw_gradient_custom(grad, bg_box, bg_start, bg_end, grad_type=gradient_type)
        arr = np.array(grad)
        arr[..., 3] = 255
        grad = Image.fromarray(arr, mode="RGBA")
        bg_mask = Image.new("L", (width, height), 0)
        bg_mask_draw = ImageDraw.Draw(bg_mask)
        draw_asym_rounded_rectangle(bg_mask_draw, bg_box, (max(0,cr_tl-border_width), max(0,cr_tr-border_width), max(0,cr_br-border_width), max(0,cr_bl-border_width)), fill=255, SS=SS)
        grad_masked = Image.new("RGBA", (width, height), (0,0,0,0))
        grad_masked.paste(grad, (0,0), mask=bg_mask)
        img = grad_masked
        if texture in TEXTURE_MAP and texture != "none":
            img = TEXTURE_MAP[texture](
                img,
                density=texture_density,
                opacity=texture_opacity,
                rotation=getattr(config, 'texture_rotation', 0),
                colors=getattr(config, 'texture_colors', None),
                SS=SS
            )
    else:
        if border:
            draw.rounded_rectangle(mask_box, radius=border_radius, fill=(200,200,200,255))
            draw.rounded_rectangle(inner_box, radius=max(0, border_radius-border_width), fill=(0,0,0,0))
        bg_box = [border_width, border_width, width-border_width-1, height-border_width-1]
        bg_radius = max(0, border_radius-border_width)
        grad = Image.new("RGBA", (width, height), (0,0,0,0))
        draw_gradient_custom(grad, bg_box, bg_start, bg_end, grad_type=gradient_type)
        arr = np.array(grad)
        arr[..., 3] = 255
        grad = Image.fromarray(arr, mode="RGBA")
        bg_mask = Image.new("L", (width, height), 0)
        bg_mask_draw = ImageDraw.Draw(bg_mask)
        bg_mask_draw.rounded_rectangle(bg_box, radius=bg_radius, fill=255)
        grad_masked = Image.new("RGBA", (width, height), (0,0,0,0))
        grad_masked.paste(grad, (0,0), mask=bg_mask)
        img = grad_masked
        if texture in TEXTURE_MAP and texture != "none":
            img = TEXTURE_MAP[texture](
                img,
                density=texture_density,
                opacity=texture_opacity,
                rotation=getattr(config, 'texture_rotation', 0),
                colors=getattr(config, 'texture_colors', None),
                SS=SS
            )
    return img 

def apply_shape(img, W, H):
    shape = Image.new("RGBA", img.size, (0,0,0,0))
    shape_draw = ImageDraw.Draw(shape)
    import math
    for i, (color, amp, freq, phase) in enumerate([
        ((0, 200, 255, 90), 0.18, 2, 0),
        ((0, 150, 255, 60), 0.13, 2.5, math.pi/3),
        ((0, 100, 255, 40), 0.09, 3, math.pi/2)
    ]):
        wave_height = int(H * amp)
        for x in range(W):
            y = int(H - wave_height * (1 + math.sin(2 * math.pi * freq * x / W + phase)))
            shape_draw.line([(x, y), (x, H)], fill=color)
    return Image.alpha_composite(img, shape) 