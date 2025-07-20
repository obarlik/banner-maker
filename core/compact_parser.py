# compact_parser.py
"""
Compact multi-value parameter parser for new CLI system.
Parses colon-separated values like "blue:purple:diagonal" into structured config.
"""

from core.color_utils import parse_color, hex_to_rgb, parse_color_to_hex
from core.constants import VALID_GRADIENTS, VALID_TEXTURES, VALID_PATTERNS, VALID_SHAPES

def parse_bg_parameter(value):
    """
    Parse background parameter: "start:end:type"
    Examples: "blue:purple:diagonal", "#ff0000:#00ff00:vertical", "red"
    """
    if not value:
        return {}
    
    parts = value.split(':')
    result = {}
    
    # First part is always start color
    if len(parts) >= 1:
        result['bg_color_start'] = parse_color_to_hex(parts[0])
    
    # Second part is end color (defaults to start color)
    if len(parts) >= 2:
        result['bg_color_end'] = parse_color_to_hex(parts[1])
    else:
        result['bg_color_end'] = result.get('bg_color_start', '#0052CC')
    
    # Third part is gradient type
    if len(parts) >= 3:
        gradient_type = parts[2].lower()
        if gradient_type in VALID_GRADIENTS:
            result['gradient_type'] = gradient_type
        else:
            result['gradient_type'] = 'vertical'
    else:
        result['gradient_type'] = 'vertical'
    
    return result

def parse_text_parameter(value):
    """
    Parse text parameter: "color:shadow"
    Examples: "white:dark", "#ffffff:true", "black"
    """
    if not value:
        return {}
    
    parts = value.split(':')
    result = {}
    
    # First part is text color
    if len(parts) >= 1:
        result['text_color'] = parse_color_to_hex(parts[0])
    
    # Second part is shadow
    if len(parts) >= 2:
        shadow_val = parts[1].lower()
        if shadow_val in ['true', 'dark', 'medium', 'soft']:
            result['shadow'] = True
            if shadow_val == 'dark':
                result['shadow_opacity'] = 150
            elif shadow_val == 'medium':
                result['shadow_opacity'] = 100
            elif shadow_val == 'soft':
                result['shadow_opacity'] = 60
        else:
            result['shadow'] = False
    
    return result

def parse_pattern_parameter(value):
    """
    Parse pattern parameter: "type:color:opacity" or "type:color:opacity:freq:amp" for wave patterns
    Examples: "dots:black:255", "stars_outline:gold:100", "sine:blue:100:3:20", "wave:red:80:2.5:15"
    """
    if not value:
        return {}
    
    parts = value.split(':')
    result = {}
    
    # First part is pattern type (now includes filled/outline in name)
    if len(parts) >= 1:
        pattern_type = parts[0].lower()
        if pattern_type in VALID_PATTERNS:
            result['pattern'] = pattern_type
        else:
            result['pattern'] = 'none'
    
    # Second part is color
    if len(parts) >= 2 and parts[1]:
        color = parse_color_to_hex(parts[1])
        result['pattern_colors'] = [color]
    else:
        # Default to black for visibility on white background
        result['pattern_colors'] = ['#000000']
    
    # Third part is opacity
    if len(parts) >= 3:
        try:
            opacity = int(parts[2])
            result['pattern_opacity'] = max(0, min(255, opacity))
        except ValueError:
            result['pattern_opacity'] = 255
    else:
        result['pattern_opacity'] = 255
    
    # Fourth and fifth parts are frequency and amplitude for wave patterns
    wave_patterns = ['sine', 'wave', 'zigzag']
    if result.get('pattern') in wave_patterns:
        # Fourth part is frequency
        if len(parts) >= 4:
            try:
                freq = float(parts[3])
                result['pattern_freq'] = max(0.5, min(10, freq))
            except ValueError:
                pass  # Use default from pattern function
        
        # Fifth part is amplitude
        if len(parts) >= 5:
            try:
                amp = float(parts[4])
                result['pattern_amp'] = max(5, min(50, amp))
            except ValueError:
                pass  # Use default from pattern function
    
    return result

def parse_shape_parameter(value):
    """
    Parse shape parameter: "type:color:opacity"
    Examples: "wave:blue:60", "circle:#ff0000:80", "ellipse:accent:40"
    """
    if not value:
        return {}
    
    parts = value.split(':')
    result = {}
    
    # First part is shape type
    if len(parts) >= 1:
        shape_type = parts[0].lower()
        if shape_type in VALID_SHAPES:
            result['shape'] = shape_type
        else:
            result['shape'] = 'none'
    
    # Second part is color (can be "accent" keyword)
    if len(parts) >= 2:
        color_val = parts[1].lower()
        if color_val == 'accent':
            # Will be resolved later by accent processor
            result['shape_use_accent'] = True
        else:
            color_rgb = hex_to_rgb(parse_color_to_hex(color_val))
            # Third part is opacity if provided
            opacity = 90
            if len(parts) >= 3:
                try:
                    opacity = int(parts[2])
                    opacity = max(0, min(255, opacity))
                except ValueError:
                    opacity = 90
            result['shape_color'] = color_rgb + (opacity,)
    
    return result

def parse_texture_parameter(value):
    """
    Parse texture parameter: "type:opacity"
    Examples: "paper:20", "metal:30", "fabric:15"
    """
    if not value:
        return {}
    
    parts = value.split(':')
    result = {}
    
    # First part is texture type
    if len(parts) >= 1:
        texture_type = parts[0].lower()
        if texture_type in VALID_TEXTURES:
            result['texture'] = texture_type
        else:
            result['texture'] = 'none'
    
    # Second part is opacity
    if len(parts) >= 2:
        try:
            opacity = int(parts[1])
            result['texture_opacity'] = max(0, min(255, opacity))
        except ValueError:
            result['texture_opacity'] = 255
    
    return result

def parse_effect_parameter(value):
    """
    Parse effect parameter: "type:intensity"
    Examples: "glow:soft", "shadow:medium", "blur:light"
    """
    if not value:
        return {}
    
    parts = value.split(':')
    result = {}
    
    # First part is effect type
    if len(parts) >= 1:
        effect_type = parts[0].lower()
        result['effect'] = effect_type
    
    # Second part is intensity
    if len(parts) >= 2:
        intensity = parts[1].lower()
        if intensity == 'soft':
            result['effect_scale'] = 0.7
        elif intensity == 'medium':
            result['effect_scale'] = 1.0
        elif intensity == 'strong':
            result['effect_scale'] = 1.5
        else:
            result['effect_scale'] = 1.0
    
    return result

def parse_multiple_values(value, parser_func):
    """
    Parse comma-separated multiple values.
    Examples: "dots:white:30,lines:gray:15" -> multiple patterns
    """
    if not value:
        return {}
    
    items = value.split(',')
    results = []
    
    for item in items:
        item = item.strip()
        if item:
            parsed = parser_func(item)
            if parsed:
                results.append(parsed)
    
    return results

def parse_compact_parameters(args):
    """
    Main function to parse all compact parameters from CLI args.
    """
    config = {}
    
    # Background
    if hasattr(args, 'bg') and args.bg:
        config.update(parse_bg_parameter(args.bg))
    
    # Text
    if hasattr(args, 'text') and args.text:
        config.update(parse_text_parameter(args.text))
    
    # Pattern (single or multiple)
    if hasattr(args, 'pattern') and args.pattern:
        if ',' in args.pattern:
            # Multiple patterns - use first one for now
            patterns = parse_multiple_values(args.pattern, parse_pattern_parameter)
            if patterns:
                config.update(patterns[0])
        else:
            config.update(parse_pattern_parameter(args.pattern))
    
    # Shape (single or multiple)
    if hasattr(args, 'shape') and args.shape:
        if ',' in args.shape:
            # Multiple shapes - use first one for now
            shapes = parse_multiple_values(args.shape, parse_shape_parameter)
            if shapes:
                config.update(shapes[0])
        else:
            config.update(parse_shape_parameter(args.shape))
    
    # Texture
    if hasattr(args, 'texture') and args.texture:
        config.update(parse_texture_parameter(args.texture))
    
    # Effect
    if hasattr(args, 'effect') and args.effect:
        config.update(parse_effect_parameter(args.effect))
    
    return config

def apply_accent_color(config, accent_color):
    """
    Apply accent color to shapes, patterns, and highlights.
    """
    accent_rgb = hex_to_rgb(parse_color_to_hex(accent_color))
    
    # Apply to shape if using accent
    if config.get('shape_use_accent'):
        opacity = config.get('shape_color', (0, 0, 0, 90))[3] if 'shape_color' in config else 90
        config['shape_color'] = accent_rgb + (opacity,)
        config.pop('shape_use_accent', None)
    
    # Apply to pattern colors if not specified
    if 'pattern' in config and config['pattern'] != 'none' and 'pattern_colors' not in config:
        config['pattern_colors'] = [parse_color_to_hex(accent_color)]
    
    return config

def apply_intensity_modifier(config, intensity):
    """
    Apply global intensity modifier to all opacity/contrast values.
    """
    multiplier = 1.0
    if intensity == 'low':
        multiplier = 0.7
    elif intensity == 'medium':
        multiplier = 1.0
    elif intensity == 'high':
        multiplier = 1.3
    
    # Apply to various opacity values
    if 'pattern_opacity' in config:
        config['pattern_opacity'] = int(min(255, config['pattern_opacity'] * multiplier))
    
    if 'texture_opacity' in config:
        config['texture_opacity'] = int(min(255, config['texture_opacity'] * multiplier))
    
    if 'shadow_opacity' in config:
        config['shadow_opacity'] = int(min(255, config['shadow_opacity'] * multiplier))
    
    if 'shape_color' in config:
        r, g, b, a = config['shape_color']
        config['shape_color'] = (r, g, b, int(min(255, a * multiplier)))
    
    return config

def apply_rounded_modifier(config, radius):
    """
    Apply global rounded corners modifier.
    """
    try:
        radius_val = int(radius)
        config['rounded'] = True
        config['corner_radius_tl'] = radius_val
        config['corner_radius_tr'] = radius_val
        config['corner_radius_bl'] = radius_val
        config['corner_radius_br'] = radius_val
    except ValueError:
        pass
    
    return config