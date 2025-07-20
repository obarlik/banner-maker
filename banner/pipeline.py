"""
Main banner generation pipeline
"""
from dataclasses import dataclass
from PIL import Image
from PIL import ImageDraw
from banner.background import create_background
from banner.background import draw_asym_rounded_rectangle
from banner.icon import add_icon
from banner.text import add_text
from banner.effects import apply_effects
from banner.patterns import PATTERN_MAP
from banner.textures import TEXTURE_MAP
from banner.overlays import OVERLAY_MAP
from banner.shapes import SHAPE_MAP
from typing import Tuple

@dataclass
class BannerConfig:
    title: str = "Banner Maker"
    subtitle: str = "Professional Banner Generation Tool"
    icon_path: str = None
    output: str = "banner.png"
    width: int = 1024
    height: int = 256
    bg_color_start: str = "#0052CC"
    bg_color_end: str = "#172B4D"
    text_color: str = "auto"  # Default: automatic contrast
    icon_bg_color: str = None
    title_font_size: int = None
    subtitle_font_size: int = None
    title_font: str = "DejaVuSansMono-Bold.ttf"
    subtitle_font: str = "DejaVuSansMono.ttf"
    icon_size: int = 120
    icon_position: str = "right"
    shadow: bool = False
    border: bool = False
    border_width: int = 4  # Default border width
    border_color: str = "#c8c8c8"  # Default border color
    rounded: bool = False
    output_format: str = "png"
    auto_color: bool = True
    gradient_type: str = "vertical"
    texture: str = "none"
    min_contrast: float = 4.5
    jitter_amount: float = 0.0    # shift ratio for dots_jittered (0.0 – 1.0)
    size_variance: float = 0.0    # size variance for dots_jittered (0.0 – 1.0)
    shadow_opacity: int = 100
    icon_shadow: bool = False
    icon_outline: bool = False
    corner_radius_tl: int = None
    corner_radius_tr: int = None
    corner_radius_bl: int = None
    corner_radius_br: int = None
    padding: int = 32
    effect: str = "none"
    effect_position: str = "top_right"  # top_left, top_right, center, bottom_left, bottom_right, custom
    effect_scale: float = 1.0           # 0.5-2.0 lens flare size multiplier
    effect_x: float = None              # Custom X coordinate (0.0-1.0, None = use effect_position)
    effect_y: float = None              # Custom Y coordinate (0.0-1.0, None = use effect_position)
    # --- New text_box parameters ---
    text_box: bool = False
    text_box_color: str = "rgba(0,0,0,0.35)"
    text_box_radius: int = 8
    text_box_padding: int = 12
    # --- New texture parameters ---
    texture_opacity: int = 255
    texture_density: float = 1.0
    texture_rotation: float = 0
    texture_colors: list = None
    texture_scale: float = 1.0
    texture_displacement_strength: float = 12.0
    texture_shading_strength: float = 4.0
    texture_contrast_boost: float = 1.0
    texture_blur: float = 0.0
    texture_seed: int = 42
    grid_spacing: int = 80
    SuperSampling: int = 2  # Supersampling factor (default 2, can be 2-3)
    pattern: str = "none"
    pattern_density: float = 1.0
    pattern_opacity: int = 255
    pattern_rotation: float = 0     # Overall pattern rotation (1D patterns)
    pattern_tilt: float = 0         # Individual motif random rotation (2D patterns)
    pattern_colors: list = None
    pattern_jitter: float = 0.0
    pattern_size_variance: float = 0.0
    pattern_freq: float = None  # Frequency for wave patterns (sine, wave, zigzag)
    pattern_amp: float = None   # Amplitude for wave patterns (sine, wave, zigzag)
    overlay: str = "none"
    
    # Debug and test mode settings
    test_mode: bool = False  # Bypasses automatic adjustments in test scenarios
    verbose: bool = False    # Show detailed configuration output
    
    shape: str = "none"
    shape_color: tuple = (0, 200, 255, 90)
    shape_blur: int = 16
    shapes: list = None  # Multi-shape configuration
    preset_name: str = None  # Preset name (for error message)

def get_layer_mask(config: BannerConfig) -> Image.Image:
    width = config.width
    height = config.height
    border = getattr(config, 'border', False)
    rounded = getattr(config, 'rounded', False)
    corner_radius_tl = getattr(config, 'corner_radius_tl', None)
    corner_radius_tr = getattr(config, 'corner_radius_tr', None)
    corner_radius_bl = getattr(config, 'corner_radius_bl', None)
    corner_radius_br = getattr(config, 'corner_radius_br', None)
    SS = getattr(config, 'SuperSampling', 1)
    border_width = getattr(config, 'border_width', 4)
    border_radius = (height // 6 if rounded else 0) * SS
    mask_box = [0, 0, width-1, height-1]
    bg_box = [border_width, border_width, width-border_width-1, height-border_width-1]
    corners = [corner_radius_tl, corner_radius_tr, corner_radius_br, corner_radius_bl]
    mask = Image.new("L", (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    if any(c is not None for c in corners):
        cr_tl = corner_radius_tl if corner_radius_tl is not None else border_radius
        cr_tr = corner_radius_tr if corner_radius_tr is not None else border_radius
        cr_br = corner_radius_br if corner_radius_br is not None else border_radius
        cr_bl = corner_radius_bl if corner_radius_bl is not None else border_radius
        draw_asym_rounded_rectangle(mask_draw, bg_box, (max(0,cr_tl-border_width), max(0,cr_tr-border_width), max(0,cr_br-border_width), max(0,cr_bl-border_width)), fill=255, SS=SS)
    else:
        bg_radius = max(0, border_radius-border_width)
        mask_draw.rounded_rectangle(bg_box, radius=bg_radius, fill=255)
    return mask

# Layer functions (no mask_layer anymore, mask will be applied at the end only)
def create_background_layer(config: BannerConfig) -> Image.Image:
    return create_background(config)

def apply_pattern_layer(img: Image.Image, config: BannerConfig) -> Image.Image:
    pattern_type = getattr(config, 'pattern', 'none')
    pattern_density = getattr(config, 'pattern_density', 1.0)
    pattern_opacity = getattr(config, 'pattern_opacity', 255)
    pattern_rotation = getattr(config, 'pattern_rotation', 0)
    pattern_tilt = getattr(config, 'pattern_tilt', 0)
    pattern_colors = getattr(config, 'pattern_colors', None)
    pattern_jitter = getattr(config, 'pattern_jitter', 0.0)
    pattern_size_variance = getattr(config, 'pattern_size_variance', 0.0)
    pattern_freq = getattr(config, 'pattern_freq', None)
    pattern_amp = getattr(config, 'pattern_amp', None)
    width = config.width
    height = config.height
    bg_box = [0, 0, width, height]
    if pattern_type in PATTERN_MAP and pattern_type != 'none':
        # Calculate expanded dimensions for rotation if needed
        if pattern_rotation != 0:
            import math
            # Calculate diagonal to ensure full coverage after rotation
            diagonal = math.sqrt(width**2 + height**2)
            expanded_width = expanded_height = int(diagonal * 1.1)  # 10% extra margin
            # Center the original area within expanded area
            offset_x = (expanded_width - width) // 2
            offset_y = (expanded_height - height) // 2
            pattern_layer = Image.new("RGBA", (expanded_width, expanded_height), (0,0,0,0))
            expanded_bg_box = [0, 0, expanded_width, expanded_height]
        else:
            pattern_layer = Image.new("RGBA", (width, height), (0,0,0,0))
            expanded_bg_box = bg_box
            offset_x = offset_y = 0
        
        # Prepare pattern parameters
        pattern_kwargs = {
            'SS': getattr(config, 'SuperSampling', 1)
        }
        
        # Add freq and amp for wave patterns
        if pattern_type in ['sine', 'wave', 'zigzag']:
            if pattern_freq is not None:
                pattern_kwargs['freq'] = pattern_freq
            if pattern_amp is not None:
                pattern_kwargs['amp'] = pattern_amp
        
        pattern_layer = PATTERN_MAP[pattern_type](
            pattern_layer, expanded_bg_box, height,  # Always use original height for density calculations
            pattern_density, pattern_opacity, pattern_jitter, pattern_size_variance, 
            pattern_rotation, pattern_tilt, pattern_colors, **pattern_kwargs
        )
        
        # Apply overall pattern rotation if specified
        if pattern_rotation != 0:
            pattern_layer = pattern_layer.rotate(pattern_rotation, expand=False, fillcolor=(0,0,0,0))
            # Crop back to original banner size from center
            left = offset_x
            top = offset_y
            right = left + width
            bottom = top + height
            pattern_layer = pattern_layer.crop((left, top, right, bottom))
        
        img = Image.alpha_composite(img, pattern_layer)
    return img

def apply_icon_layer(img: Image.Image, config: BannerConfig) -> Image.Image:
    return add_icon(img, config)

def apply_text_layer(img: Image.Image, config: BannerConfig) -> Image.Image:
    return add_text(img, config)

def apply_texture_layer(img: Image.Image, config: BannerConfig) -> Image.Image:
    texture = getattr(config, 'texture', 'none')
    if texture in TEXTURE_MAP and texture != 'none':
        img = TEXTURE_MAP[texture](
            img,
            density=getattr(config, 'texture_density', 1.0),
            opacity=getattr(config, 'texture_opacity', 255),
            rotation=getattr(config, 'texture_rotation', 0),
            colors=getattr(config, 'texture_colors', None),
            SS=getattr(config, 'SuperSampling', 1),
            scale=getattr(config, 'texture_scale', 1.0),
            displacement_strength=getattr(config, 'texture_displacement_strength', 12.0),
            shading_strength=getattr(config, 'texture_shading_strength', 4.0),
            contrast_boost=getattr(config, 'texture_contrast_boost', 1.0),
            blur=getattr(config, 'texture_blur', 0.0),
            seed=getattr(config, 'texture_seed', 42),
            grid_spacing=getattr(config, 'grid_spacing', 80)
        )
    return img

def apply_effects_layer(img: Image.Image, config: BannerConfig) -> Image.Image:
    return apply_effects(img, config)

def apply_overlay_layer(img: Image.Image, config: BannerConfig) -> Image.Image:
    overlay_type = getattr(config, 'overlay', 'none')
    if overlay_type == 'none' or overlay_type not in OVERLAY_MAP:
        return img
    width = getattr(config, 'width', 1024)
    height = getattr(config, 'height', 256)
    SS = getattr(config, 'SuperSampling', 1)
    overlay_func = OVERLAY_MAP[overlay_type]
    # collect parameters starting with overlay_
    params = {}
    for key, value in config.__dict__.items():
        if key.startswith('overlay_'):
            param_name = key.replace('overlay_', '')
            params[param_name] = value
    return overlay_func(img, width, height, SS, **params)


def apply_shape_layer(img: Image.Image, config: BannerConfig) -> Image.Image:
    # Check for multi-shape configuration
    shapes = getattr(config, 'shapes', None)
    if shapes:
        # Multi-shape system
        width = getattr(config, 'width', 1024)
        height = getattr(config, 'height', 256)
        SS = getattr(config, 'SuperSampling', 1)
        
        for shape_config in shapes:
            shape_type = shape_config.get('type', 'none')
            if shape_type in SHAPE_MAP:
                shape_func = SHAPE_MAP[shape_type]
                # Use shape_config directly as parameters (minus 'type')
                params = {k: v for k, v in shape_config.items() if k != 'type'}
                img = shape_func(img, width, height, SS, **params)
        return img
    
    # Single shape system (backward compatibility)
    shape_type = getattr(config, 'shape', 'none')
    if shape_type == 'none' or shape_type not in SHAPE_MAP:
        return img
    width = getattr(config, 'width', 1024)
    height = getattr(config, 'height', 256)
    SS = getattr(config, 'SuperSampling', 1)
    shape_func = SHAPE_MAP[shape_type]
    # collect parameters starting with shape_
    params = {}
    for key, value in config.__dict__.items():
        if key.startswith('shape_'):
            param_name = key.replace('shape_', '')
            params[param_name] = value
    return shape_func(img, width, height, SS, **params)

def apply_mask_layer(img: Image.Image, config: BannerConfig) -> Image.Image:
    mask = get_layer_mask(config)
    masked = Image.new("RGBA", img.size, (0,0,0,0))
    masked.paste(img, (0,0), mask=mask)
    return masked

def apply_border_layer(img: Image.Image, config: BannerConfig) -> Image.Image:
    border = getattr(config, 'border', False)
    if not border:
        return img
    width, height = img.size
    SS = getattr(config, 'SuperSampling', 1)
    border_width = getattr(config, 'border_width', 4) * SS
    border_color = getattr(config, 'border_color', "#c8c8c8")
    # Convert color string to RGBA tuple if needed
    if isinstance(border_color, str):
        from core.image_utils import hex_to_rgb
        rgb = hex_to_rgb(border_color)
        border_color = rgb + (255,)
    corner_radius_tl = getattr(config, 'corner_radius_tl', None)
    corner_radius_tr = getattr(config, 'corner_radius_tr', None)
    corner_radius_bl = getattr(config, 'corner_radius_bl', None)
    corner_radius_br = getattr(config, 'corner_radius_br', None)
    rounded = getattr(config, 'rounded', False)
    border_radius = (height // 6 if rounded else 0) * SS
    cr_tl = corner_radius_tl if corner_radius_tl is not None else border_radius
    cr_tr = corner_radius_tr if corner_radius_tr is not None else border_radius
    cr_br = corner_radius_br if corner_radius_br is not None else border_radius
    cr_bl = corner_radius_bl if corner_radius_bl is not None else border_radius
    border_layer = Image.new("RGBA", (width, height), (0,0,0,0))
    border_draw = ImageDraw.Draw(border_layer)
    from banner.background import draw_asym_rounded_rectangle
    draw_asym_rounded_rectangle(border_draw, [0,0,width-1,height-1], (cr_tl, cr_tr, cr_br, cr_bl), fill=None, outline=border_color, width=border_width, SS=SS)
    return Image.alpha_composite(img, border_layer)

def resize_and_save(img: Image.Image, orig_size: Tuple[int, int], output: str):
    final_img = img.resize(orig_size, resample=Image.LANCZOS)
    final_img.save(output, format="PNG")
    print(f"Banner saved as {output}")

# Main pipeline function

def generate_banner(config: BannerConfig):
    SS = getattr(config, 'SuperSampling', 2)
    # Ensure SS is within valid range
    SS = max(2, min(3, SS))
    orig_width = getattr(config, 'width', 1024)
    orig_height = getattr(config, 'height', 256)
    big_config = BannerConfig(**{
        **config.__dict__,
        'width': orig_width*SS,
        'height': orig_height*SS,
        'SuperSampling': SS,
        'corner_radius_tl': config.corner_radius_tl * SS if config.corner_radius_tl is not None else None,
        'corner_radius_tr': config.corner_radius_tr * SS if config.corner_radius_tr is not None else None,
        'corner_radius_bl': config.corner_radius_bl * SS if config.corner_radius_bl is not None else None,
        'corner_radius_br': config.corner_radius_br * SS if config.corner_radius_br is not None else None,
        'preset_name': getattr(config, 'preset_name', None),
    })
    try:
        img = create_background_layer(big_config)
        img = apply_pattern_layer(img, big_config)     # Pattern behind everything
        img = apply_shape_layer(img, big_config)     # Decorative shapes behind text/icon
        img = apply_icon_layer(img, big_config)      # Icon in foreground
        img = apply_text_layer(img, big_config)      # Text on top of everything
        img = apply_texture_layer(img, big_config)
        img = apply_effects_layer(img, big_config)
        img = apply_overlay_layer(img, big_config)
        img = apply_mask_layer(img, big_config)
        img = apply_border_layer(img, big_config)
        resize_and_save(img, (orig_width, orig_height), config.output)
    except Exception as e:
        import traceback
        import pprint
        tb = traceback.format_exc()
        layer = "Unknown"
        for l in [
            "create_background_layer", "apply_pattern_layer", "apply_shape_layer", "apply_icon_layer", "apply_text_layer", "apply_texture_layer", "apply_effects_layer", "apply_overlay_layer", "apply_mask_layer", "apply_border_layer"
        ]:
            if l in tb:
                layer = l
                break
        preset_name = getattr(config, 'preset_name', None)
        config_dict = dict(big_config.__dict__)
        config_str = pprint.pformat(config_dict, width=120, compact=True)
        raise RuntimeError(
            f"[ERROR] Layer: {layer} | Preset: {preset_name or 'Unknown'} | Error: {str(e)}\n\nUsed config parameters:\n{config_str}\n\nDetailed traceback:\n{tb}"
        ) from e 