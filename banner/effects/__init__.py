# effects/__init__.py
# Auto-discovery and import of effect modules

import os
import importlib

# Get current directory
current_dir = os.path.dirname(__file__)

# Auto-discover effect files
effect_files = [f[:-3] for f in os.listdir(current_dir) 
                if f.endswith('.py') and f != '__init__.py' and not f.startswith('_')]

# Build EFFECT_MAP by importing modules
EFFECT_MAP = {}
for effect_name in effect_files:
    try:
        module = importlib.import_module(f'.{effect_name}', package='banner.effects')
        if hasattr(module, f'apply_{effect_name}'):
            EFFECT_MAP[effect_name] = getattr(module, f'apply_{effect_name}')
    except ImportError:
        pass

# Add special handling for lens_flare which has different parameter signature
if 'lens_flare' in EFFECT_MAP:
    # Keep the original lens_flare function with its full signature
    pass

def apply_effects(img, config):
    """Applies extra effects."""
    from PIL import Image, ImageDraw
    from core.geometry_utils import draw_asym_rounded_rectangle
    
    effect = getattr(config, 'effect', 'none')
    effect_position = getattr(config, 'effect_position', 'top_right')
    effect_scale = getattr(config, 'effect_scale', 1.0)
    effect_x = getattr(config, 'effect_x', None)
    effect_y = getattr(config, 'effect_y', None)
    width = getattr(config, 'width', 1024)
    height = getattr(config, 'height', 256)
    SS = getattr(config, 'SuperSampling', 1)
    W, H = width, height
    # Mask parametreleri
    border = getattr(config, 'border', False)
    rounded = getattr(config, 'rounded', False)
    corner_radius_tl = getattr(config, 'corner_radius_tl', None)
    corner_radius_tr = getattr(config, 'corner_radius_tr', None)
    corner_radius_bl = getattr(config, 'corner_radius_bl', None)
    corner_radius_br = getattr(config, 'corner_radius_br', None)
    border_radius = (height // 6 if rounded else 0) * SS
    border_width = (4 if border else 0) * SS
    mask_box = [0, 0, W-1, H-1]
    bg_box = [border_width, border_width, W-border_width-1, H-border_width-1]
    # Create mask
    corners = [corner_radius_tl, corner_radius_tr, corner_radius_br, corner_radius_bl]
    mask = Image.new("L", (W, H), 0)
    mask_draw = ImageDraw.Draw(mask)
    if any(c is not None for c in corners):
        cr_tl = (corner_radius_tl if corner_radius_tl is not None else border_radius) * SS
        cr_tr = (corner_radius_tr if corner_radius_tr is not None else border_radius) * SS
        cr_br = (corner_radius_br if corner_radius_br is not None else border_radius) * SS
        cr_bl = (corner_radius_bl if corner_radius_bl is not None else border_radius) * SS
        draw_asym_rounded_rectangle(mask_draw, bg_box, (max(0,cr_tl-border_width), max(0,cr_tr-border_width), max(0,cr_br-border_width), max(0,cr_bl-border_width)), fill=255)
    else:
        bg_radius = max(0, border_radius-border_width)
        mask_draw.rounded_rectangle(bg_box, radius=bg_radius, fill=255)

    if isinstance(effect, str):
        effect_list = [e.strip() for e in effect.split(",") if e.strip() and e.strip() != "none"]
    else:
        effect_list = list(effect)
    for effect_name in effect_list:
        if effect_name in EFFECT_MAP:
            # Apply filter effect to entire image
            if effect_name == "lens_flare":
                # Enhanced lens flare with full customization
                core_color = getattr(config, 'flare_core_color', (255, 255, 255))
                ghost_colors = getattr(config, 'flare_ghost_colors', None)
                intensity = getattr(config, 'flare_intensity', 1.0)
                spike_enabled = getattr(config, 'flare_spikes', True)
                hexagon_enabled = getattr(config, 'flare_hexagon', True)
                blur_layers = getattr(config, 'flare_blur_layers', 3)
                img = EFFECT_MAP[effect_name](img, position=effect_position, scale=effect_scale, SS=SS,
                                       custom_x=effect_x, custom_y=effect_y, core_color=core_color,
                                       ghost_colors=ghost_colors, intensity=intensity,
                                       spike_enabled=spike_enabled, hexagon_enabled=hexagon_enabled,
                                       blur_layers=blur_layers)
            else:
                img = EFFECT_MAP[effect_name](img)
            
            # Apply mask to final result
            img_masked = Image.new("RGBA", img.size, (0,0,0,0))
            img_masked.paste(img, (0,0), mask=mask)
            img = img_masked
    return img

# Export the map
__all__ = ['EFFECT_MAP', 'apply_effects']