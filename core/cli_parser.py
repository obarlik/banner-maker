# cli_parser_v2.py
"""
New CLI parser for compact multi-value parameter system.
Integrates with existing BannerConfig while providing modern CLI interface.
"""

import argparse
import sys
from core.parameter_definitions import ALL_PARAMETERS, get_parameter_help, get_parameter_short_help
from core.compact_parser import parse_compact_parameters, apply_accent_color, apply_intensity_modifier, apply_rounded_modifier
from core.preset import load_preset
from banner.pipeline import BannerConfig

def create_new_argument_parser():
    """Create argument parser with new compact parameter system."""
    parser = argparse.ArgumentParser(
        description='Banner Maker - Professional banner generation tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=get_parameter_short_help()
    )
    
    # Core parameters
    parser.add_argument('--title', type=str, help='Project title text')
    parser.add_argument('--subtitle', type=str, help='Project subtitle/description text')
    parser.add_argument('--icon', type=str, help='Path to icon image file')
    parser.add_argument('--output', type=str, help='Output file name')
    parser.add_argument('--preset', type=str, help='Use design preset (modern_blue, ocean_waves, etc.)')
    
    # Visual design parameters (compact multi-value)
    parser.add_argument('--bg', type=str, help='Background colors and gradient type (start:end:type)')
    parser.add_argument('--text', type=str, help='Text color and shadow (color:shadow)')
    parser.add_argument('--accent', type=str, help='Accent color (auto-applies to shapes, patterns, highlights)')
    
    # Design element parameters
    parser.add_argument('--pattern', type=str, help='Background pattern/motif (type:color:opacity)')
    parser.add_argument('--shape', type=str, help='Decorative shape element (type:color:opacity)')
    parser.add_argument('--texture', type=str, help='Background texture (type:opacity)')
    parser.add_argument('--effect', type=str, help='Visual effect (type:intensity)')
    
    # Style parameters
    parser.add_argument('--rounded', type=str, help='Corner radius (0-50)')
    parser.add_argument('--padding', type=str, help='Internal spacing (20-60)')
    parser.add_argument('--size', type=str, help='Overall size scale (small/medium/large)')
    
    # Smart modifier parameters
    parser.add_argument('--intensity', type=str, help='Global intensity modifier (low/medium/high)')
    parser.add_argument('--contrast', type=str, help='Global contrast modifier (low/medium/high)')
    
    # System parameters
    parser.add_argument('--demo', action='store_true', help='Generate demo banner set')
    parser.add_argument('--verbose', action='store_true', help='Show detailed configuration output')
    
    # Help options
    parser.add_argument('--help-full', action='store_true', help='Show detailed parameter documentation')
    parser.add_argument('--learn', type=str, help='Show CLI equivalent of preset')
    parser.add_argument('--test-element', type=str, help='Test specific element in isolation (background, text, icon, pattern, shape, texture, effect)')
    
    return parser

def resolve_preset_config(preset_name):
    """Load and resolve preset configuration."""
    if not preset_name:
        return {}
    
    try:
        preset_config = load_preset(preset_name)
        if preset_config:
            return preset_config
        else:
            print(f"Warning: Preset '{preset_name}' not found. Using defaults.")
            return {}
    except Exception as e:
        print(f"Error loading preset '{preset_name}': {e}")
        return {}

def apply_size_modifier(config, size):
    """Apply size modifier to fonts and spacing."""
    if not size:
        return config
    
    size = size.lower()
    
    # Size multipliers
    multipliers = {
        'small': 0.8,
        'medium': 1.0,
        'large': 1.2
    }
    
    if size in multipliers:
        mult = multipliers[size]
        
        # Apply to padding
        if 'padding' not in config:
            config['padding'] = int(32 * mult)
        
        # Apply to icon size
        if 'icon_size' not in config:
            config['icon_size'] = int(120 * mult)
        
        # Title and subtitle font sizes will be auto-calculated
        # but we can set hints for the auto-sizing system
        if mult != 1.0:
            config['_size_modifier'] = mult
    
    return config

def apply_contrast_modifier(config, contrast):
    """Apply contrast modifier to text and background."""
    if not contrast:
        return config
    
    contrast = contrast.lower()
    
    # Contrast levels
    contrast_levels = {
        'low': 3.0,
        'medium': 4.5,
        'high': 7.0
    }
    
    if contrast in contrast_levels:
        config['min_contrast'] = contrast_levels[contrast]
    
    return config

def apply_padding_modifier(config, padding):
    """Apply padding modifier."""
    if not padding:
        return config
    
    try:
        padding_val = int(padding)
        config['padding'] = max(10, min(100, padding_val))
    except ValueError:
        pass
    
    return config

def show_preset_cli_equivalent(preset_name):
    """Show CLI equivalent of a preset."""
    preset_config = resolve_preset_config(preset_name)
    if not preset_config:
        print(f"Preset '{preset_name}' not found.")
        return
    
    cli_parts = []
    
    # Background
    if 'bg_color_start' in preset_config and 'bg_color_end' in preset_config:
        bg_type = preset_config.get('gradient_type', 'vertical')
        cli_parts.append(f"--bg \"{preset_config['bg_color_start']}:{preset_config['bg_color_end']}:{bg_type}\"")
    
    # Pattern
    if preset_config.get('pattern', 'none') != 'none':
        pattern_color = preset_config.get('pattern_colors', ['#ffffff'])[0]
        pattern_opacity = preset_config.get('pattern_opacity', 255)
        cli_parts.append(f"--pattern \"{preset_config['pattern']}:{pattern_color}:{pattern_opacity}\"")
    
    # Shape
    if preset_config.get('shape', 'none') != 'none':
        shape_color = preset_config.get('shape_color', (100, 150, 255, 60))
        color_hex = f"#{shape_color[0]:02x}{shape_color[1]:02x}{shape_color[2]:02x}"
        cli_parts.append(f"--shape \"{preset_config['shape']}:{color_hex}:{shape_color[3]}\"")
    
    # Texture
    if preset_config.get('texture', 'none') != 'none':
        texture_opacity = preset_config.get('texture_opacity', 255)
        cli_parts.append(f"--texture \"{preset_config['texture']}:{texture_opacity}\"")
    
    # Rounded corners
    if preset_config.get('rounded', False):
        radius = preset_config.get('corner_radius_tl', 0)
        if radius > 0:
            cli_parts.append(f"--rounded \"{radius}\"")
    
    # Text shadow
    if preset_config.get('shadow', False):
        shadow_opacity = preset_config.get('shadow_opacity', 100)
        shadow_type = 'soft' if shadow_opacity < 80 else 'medium' if shadow_opacity < 120 else 'dark'
        text_color = preset_config.get('text_color', 'auto')
        cli_parts.append(f"--text \"{text_color}:{shadow_type}\"")
    
    print(f"CLI equivalent of preset '{preset_name}':")
    print()
    if cli_parts:
        print(f"python banner_maker.py --title \"Your Title\" {' '.join(cli_parts)}")
    else:
        print(f"python banner_maker.py --preset {preset_name} --title \"Your Title\"")
    print()

def generate_isolated_element_test(config, element_name):
    """Generate banner with only the specified element."""
    from banner.pipeline import (
        create_background_layer, apply_pattern_layer, apply_shape_layer,
        apply_icon_layer, apply_text_layer, apply_texture_layer, 
        apply_effects_layer, resize_and_save
    )
    from PIL import Image
    
    # SuperSampling setup
    SS = getattr(config, 'SuperSampling', 2)
    orig_width = config.width
    orig_height = config.height
    
    # Create supersampled config
    big_config = type(config)(**{
        **config.__dict__,
        'width': orig_width * SS,
        'height': orig_height * SS,
        'SuperSampling': SS
    })
    
    # Start with background (always needed)
    img = create_background_layer(big_config)
    
    # Apply ONLY the requested element
    if element_name == 'background':
        # Background is already applied, nothing more needed
        pass
    elif element_name == 'pattern':
        img = apply_pattern_layer(img, big_config)
    elif element_name == 'shape':
        img = apply_shape_layer(img, big_config)
    elif element_name == 'icon':
        img = apply_icon_layer(img, big_config)
    elif element_name == 'text':
        img = apply_text_layer(img, big_config)
    elif element_name == 'texture':
        img = apply_texture_layer(img, big_config)
    elif element_name == 'effect':
        # Effect needs some content to work on - add shapes and patterns
        img = apply_shape_layer(img, big_config)
        img = apply_pattern_layer(img, big_config)
        img = apply_effects_layer(img, big_config)
    
    # Save the result
    resize_and_save(img, (orig_width, orig_height), config.output)

def test_element_isolation(element_name, args):
    """Test specific element in isolation."""
    # Auto-generate valid elements list from available maps and core elements
    valid_elements = []
    
    # Core elements that don't use maps
    valid_elements.extend(['background', 'text', 'icon'])
    
    # Elements that use maps - auto-detect available maps
    try:
        from banner.patterns import PATTERN_MAP
        if PATTERN_MAP:
            valid_elements.append('pattern')
    except ImportError:
        pass
    
    try:
        from banner.shapes import SHAPE_MAP
        if SHAPE_MAP:
            valid_elements.append('shape')
    except ImportError:
        pass
    
    try:
        from banner.textures import TEXTURE_MAP
        if TEXTURE_MAP:
            valid_elements.append('texture')
    except ImportError:
        pass
    
    try:
        from banner.effects import EFFECT_MAP
        if EFFECT_MAP:
            valid_elements.append('effect')
    except ImportError:
        pass
    
    # Handle special cases
    if element_name == 'all':
        # Test all elements
        for elem in valid_elements:
            if elem in ['background', 'pattern', 'shape', 'texture', 'effect']:
                test_all_element_variations(elem, args)
            else:
                test_single_element(elem, args)
        return
    
    # Handle comma-separated list
    if ',' in element_name:
        elements = [e.strip() for e in element_name.split(',')]
        for elem in elements:
            if elem in valid_elements:
                if elem in ['background', 'pattern', 'shape', 'texture', 'effect']:
                    test_all_element_variations(elem, args)
                else:
                    test_single_element(elem, args)
            else:
                print(f"Invalid element '{elem}'. Valid elements: {', '.join(valid_elements)}")
        return
    
    if element_name not in valid_elements:
        print(f"Invalid element '{element_name}'. Valid elements:")
        for elem in valid_elements:
            print(f"  - {elem}")
        print("Use 'all' to test all elements or comma-separated list: 'pattern,shape,texture'")
        return
    
    # Single element test
    if element_name in ['background', 'pattern', 'shape', 'texture', 'effect']:
        test_all_element_variations(element_name, args)
    else:
        test_single_element(element_name, args)

def test_single_element(element_name, args):
    """Test a single element in isolation."""
    from banner.pipeline import BannerConfig, generate_banner
    import datetime
    import os
    
    # Use fixed session folder for coordinated testing
    session_dir = "tests/2025-07-14_element_tests"
    element_dir = f"{session_dir}/{element_name}s"  # shapes, textures, patterns, effects, etc.
    
    # Create directories if they don't exist
    os.makedirs(element_dir, exist_ok=True)
    
    # Determine specific element type for filename
    if element_name == 'shape' and args.shape:
        filename = f"{args.shape.split(':')[0]}.png"
    elif element_name == 'texture' and args.texture:
        filename = f"{args.texture.split(':')[0]}.png"
    elif element_name == 'pattern' and args.pattern:
        pattern_parts = args.pattern.split(':')
        pattern_type = pattern_parts[0]
        # Check if filled parameter is specified
        if len(pattern_parts) >= 4:
            fill_type = pattern_parts[3].lower()
            if fill_type == 'outline':
                filename = f"{pattern_type}_outline.png"
            else:
                filename = f"{pattern_type}_filled.png"
        else:
            filename = f"{pattern_type}_filled.png"  # Default to filled
    elif element_name == 'effect' and args.effect:
        filename = f"{args.effect.split(':')[0]}.png"
    elif element_name == 'background' and args.bg:
        bg_parts = args.bg.split(':')
        if len(bg_parts) >= 3:
            color1, color2, bg_type = bg_parts[0], bg_parts[1], bg_parts[2]
            filename = f"{color1}_{color2}_{bg_type}.png"
        else:
            filename = f"default.png"
    else:
        filename = f"default.png"
    
    # Base minimal config - square format for testing
    # ALL elements disabled by default, only enable what we're testing
    config = BannerConfig(
        title="",  # No title
        subtitle="",  # No subtitle
        output=f"{element_dir}/{filename}",
        width=512,  # Square format
        height=512,
        bg_color_start="#ffffff",  # White background
        bg_color_end="#ffffff",
        gradient_type="vertical",
        pattern="none",  # No pattern
        shape="none",  # No shape
        texture="none",  # No texture
        effect="none",  # No effect
        rounded=False,
        shadow=False,
        icon_path=None,  # No icon
        padding=0,  # No padding
        border=False,  # No border
        overlay="none"  # No overlay
    )
    
    # Apply element-specific settings - ONLY enable what we're testing
    if element_name == 'background':
        # Only background, nothing else
        if args.bg:
            from core.compact_parser import parse_bg_parameter
            bg_config = parse_bg_parameter(args.bg)
            for key, value in bg_config.items():
                setattr(config, key, value)
        else:
            config.bg_color_start = "#4285f4"
            config.bg_color_end = "#34a853"
            config.gradient_type = "diagonal"
    
    elif element_name == 'text':
        # Only text, neutral background
        config.title = "Sample Text"
        config.subtitle = "Element Test"
        config.bg_color_start = "#2c3e50"  # Dark background to see text
        config.bg_color_end = "#2c3e50"
        if args.text:
            from core.compact_parser import parse_text_parameter
            text_config = parse_text_parameter(args.text)
            for key, value in text_config.items():
                setattr(config, key, value)
        else:
            config.text_color = "#ffffff"
            config.shadow = True
            config.shadow_opacity = 120
    
    elif element_name == 'icon':
        # Only icon, neutral background
        config.bg_color_start = "#f8f9fa"
        config.bg_color_end = "#f8f9fa"
        if args.icon:
            config.icon_path = args.icon
        else:
            config.icon_path = "logo.png"  # Default test icon
        config.icon_size = 256  # Bigger in square format
        config.icon_position = "right"
    
    elif element_name == 'pattern':
        # Only pattern, white background for visibility
        config.bg_color_start = "#ffffff"
        config.bg_color_end = "#ffffff"
        if args.pattern:
            from core.compact_parser import parse_pattern_parameter
            pattern_config = parse_pattern_parameter(args.pattern)
            for key, value in pattern_config.items():
                setattr(config, key, value)
            # Don't override color from compact parser
        else:
            config.pattern = "dots"
            config.pattern_colors = ["#000000"]  # Black on white
            config.pattern_opacity = 255
    
    elif element_name == 'shape':
        # Only shape, neutral background
        config.bg_color_start = "#f8f9fa"
        config.bg_color_end = "#f8f9fa"
        if args.shape:
            from core.compact_parser import parse_shape_parameter
            shape_config = parse_shape_parameter(args.shape)
            for key, value in shape_config.items():
                setattr(config, key, value)
        else:
            config.shape = "wave"
            config.shape_color = (100, 150, 255, 150)
    
    elif element_name == 'texture':
        # Texture on medium gray background to show texture details
        config.bg_color_start = "#888888"
        config.bg_color_end = "#888888"
        if args.texture:
            from core.compact_parser import parse_texture_parameter
            texture_config = parse_texture_parameter(args.texture)
            for key, value in texture_config.items():
                setattr(config, key, value)
        else:
            config.texture = "paper"
            config.texture_opacity = 80
    
    elif element_name == 'effect':
        # Effect test - simple gradient background with basic shapes
        config.bg_color_start = "#4c7ce3"  # Blue
        config.bg_color_end = "#8b5cf6"    # Purple
        config.gradient_type = "diagonal"
        # Add simple shapes to see effect on
        config.shape = "circle"
        config.shape_color = (255, 255, 255, 180)  # Semi-transparent white
        config.pattern = "dots"
        config.pattern_colors = ["#ffffff"]
        config.pattern_opacity = 120
        config.pattern_density = 0.5
        if args.effect:
            from core.compact_parser import parse_effect_parameter
            effect_config = parse_effect_parameter(args.effect)
            for key, value in effect_config.items():
                setattr(config, key, value)
        else:
            config.effect = "glow"
            config.effect_scale = 1.0
    
    print(f"Testing element: {element_name}")
    print(f"Output file: {config.output}")
    print()
    
    # Generate banner with isolated element using custom pipeline
    generate_isolated_element_test(config, element_name)
    
    print(f"Element test completed. Check {config.output}")
    print()
    print("Other test examples:")
    print(f"  python banner_maker.py --test-element {element_name} --bg \"blue:purple:diagonal\"")
    print(f"  python banner_maker.py --test-element {element_name} --pattern \"dots:white:30\"")
    print(f"  python banner_maker.py --test-element {element_name} --shape \"wave:red:60\"")

def get_optimal_test_background(element_name, variant_name):
    """Get optimal background color for testing specific element variants."""
    
    # Single background color per element type for consistent comparison
    if element_name == 'pattern':
        # Pattern tests: ALWAYS white background for maximum contrast with black patterns
        return "#ffffff"  # Pure white for all patterns
    
    elif element_name == 'shape':
        # Shapes: single light gray background to see all shape variations
        return "#e9ecef"  # Light gray to see both light and dark shapes
    
    elif element_name == 'texture':
        # Textures: single medium gray background for all texture comparisons
        return "#6c757d"  # Medium gray that works for most textures
    
    elif element_name == 'effect':
        # Effects: single medium gray background for all effect comparisons
        return "#636e72"  # Medium gray that shows most effects well
    
    else:
        # Default: white background for text, icon, background elements
        return "#ffffff"

def get_optimal_shape_color(shape_name, bg_color):
    """Get optimal shape color for visibility against background."""
    
    # Shape colors optimized for visibility and aesthetics
    shape_colors = {
        'wave': (66, 133, 244),    # Blue wave
        'circle': (234, 67, 53),   # Red circle
        'triangle': (52, 168, 83), # Green triangle
        'rectangle': (156, 39, 176), # Purple rectangle
        'ellipse': (255, 152, 0),  # Orange ellipse
        'polygon': (0, 188, 212),  # Cyan polygon
        'blob': (233, 30, 99),     # Pink blob
        'diagonal_bar': (255, 193, 7), # Yellow diagonal bar
    }
    
    # Return RGB color tuple
    return shape_colors.get(shape_name, (0, 0, 0))  # Default to black

def test_all_element_variations(element_name, args):
    """Test all variations of a specific element type."""
    from banner.pipeline import BannerConfig, generate_banner
    import os
    
    # AUTO-GENERATE variations from existing maps - no hardcoding needed!
    def get_element_variations(element_type):
        if element_type == 'background':
            # Test all gradient types with single color pair
            return [
                ('horizontal', 'red:blue:horizontal', 100),
                ('vertical', 'red:blue:vertical', 100),
                ('diagonal', 'red:blue:diagonal', 100),
                ('radial', 'red:blue:radial', 100),
            ]
        elif element_type == 'pattern':
            # Auto-generate from PATTERN_MAP
            from banner.patterns import PATTERN_MAP
            return [(name, 'black', 255) for name in PATTERN_MAP.keys()]
        elif element_type == 'shape':
            # Auto-generate from SHAPE_MAP
            from banner.shapes import SHAPE_MAP
            return [(name, 'default', 100) for name in SHAPE_MAP.keys()]
        elif element_type == 'texture':
            # Auto-generate from TEXTURE_MAP
            from banner.textures import TEXTURE_MAP
            return [(name, 'default', 150) for name in TEXTURE_MAP.keys()]
        elif element_type == 'effect':
            # Auto-generate from EFFECT_MAP
            from banner.effects import EFFECT_MAP
            return [(name, 'default', 85) for name in EFFECT_MAP.keys()]
        else:
            return []
    
    variations = get_element_variations(element_name)
    
    if not variations:
        print(f"No variations defined for element: {element_name}")
        return
    
    # Create test directory
    session_dir = "tests/2025-07-14_element_tests"
    element_dir = f"{session_dir}/{element_name}s"
    os.makedirs(element_dir, exist_ok=True)
    
    total_variations = len(variations)
    
    print(f"Testing {total_variations} variations of {element_name}:")
    
    for i, (variant_name, color, opacity) in enumerate(variations, 1):
        print(f"  [{i}/{total_variations}] Testing {variant_name}...")
        
        # Determine optimal background color for element visibility
        bg_color = get_optimal_test_background(element_name, variant_name)
        
        # Base config - optimal background for element visibility
        config = BannerConfig(
            title="",
            subtitle="",
            output=f"{element_dir}/{variant_name}.png",
            width=512,
            height=512,
            bg_color_start=bg_color,
            bg_color_end=bg_color,
            gradient_type="vertical",
            pattern="none",
            shape="none",
            texture="none",
            effect="none",
            rounded=False,
            shadow=False,
            icon_path=None,
            padding=0,
            border=False,
            overlay="none"
        )
        
        # Configure specific element
        if element_name == 'background':
            # Parse background parameter (color format is "red:blue:horizontal")
            from core.compact_parser import parse_bg_parameter
            bg_config = parse_bg_parameter(color)
            for key, value in bg_config.items():
                setattr(config, key, value)
        elif element_name == 'pattern':
            config.pattern = variant_name
            config.pattern_colors = ["#000000"]  # Always black in test mode
            config.pattern_opacity = 255  # Full opacity for clear visibility
            # Force white background for pattern tests
            config.bg_color_start = "#ffffff"
            config.bg_color_end = "#ffffff"
            config.gradient_type = "none"  # No gradient, solid color
        elif element_name == 'shape':
            config.shape = variant_name
            # Get optimal shape color for visibility against background
            shape_color = get_optimal_shape_color(variant_name, bg_color)
            config.shape_color = (*shape_color, opacity)
        elif element_name == 'texture':
            config.texture = variant_name
            config.texture_opacity = opacity
        elif element_name == 'effect':
            config.effect = variant_name
            config.effect_scale = opacity / 100.0
            # Effects need consistent content to show effect differences
            config.pattern = "circles"  # Add pattern content
            config.pattern_colors = ["#ffffff"]  # White circles for consistent contrast
            config.pattern_opacity = 150
            config.shape = "ellipse"  # Add shape content
            config.shape_color = (255, 255, 255, 100)  # White ellipse for consistent base
        
        # Generate test
        try:
            generate_isolated_element_test(config, element_name)
            print(f"      OK {variant_name}.png created")
        except Exception as e:
            print(f"      ERROR {variant_name}.png failed: {e}")
    
    print(f"\n{element_name} testing completed. Check {element_dir}/ for results.")
    print()

def parse_new_cli_arguments(args=None):
    """Parse CLI arguments using new compact parameter system."""
    parser = create_new_argument_parser()
    
    if args is None:
        args = sys.argv[1:]
    
    parsed_args = parser.parse_args(args)
    
    # Handle special commands
    if parsed_args.help_full:
        print(get_parameter_help())
        sys.exit(0)
    
    if parsed_args.learn:
        show_preset_cli_equivalent(parsed_args.learn)
        sys.exit(0)
    
    if parsed_args.test_element:
        test_element_isolation(parsed_args.test_element, parsed_args)
        sys.exit(0)
    
    # Start with preset configuration
    config = resolve_preset_config(parsed_args.preset)
    
    # Parse compact parameters
    compact_config = parse_compact_parameters(parsed_args)
    
    # Override preset with compact parameters
    config.update(compact_config)
    
    # Apply simple overrides
    if parsed_args.title:
        config['title'] = parsed_args.title
    if parsed_args.subtitle:
        config['subtitle'] = parsed_args.subtitle
    if parsed_args.icon:
        config['icon_path'] = parsed_args.icon
    if parsed_args.output:
        config['output'] = parsed_args.output
    
    # Apply smart modifiers
    if parsed_args.accent:
        config = apply_accent_color(config, parsed_args.accent)
    if parsed_args.intensity:
        config = apply_intensity_modifier(config, parsed_args.intensity)
    if parsed_args.contrast:
        config = apply_contrast_modifier(config, parsed_args.contrast)
    if parsed_args.size:
        config = apply_size_modifier(config, parsed_args.size)
    if parsed_args.rounded:
        config = apply_rounded_modifier(config, parsed_args.rounded)
    if parsed_args.padding:
        config = apply_padding_modifier(config, parsed_args.padding)
    
    # Handle system parameters
    if parsed_args.demo:
        config['demo'] = True
    
    # Store preset name for error reporting
    if parsed_args.preset:
        config['preset_name'] = parsed_args.preset
    
    return config

def convert_to_banner_config(config_dict):
    """Convert parsed configuration to BannerConfig object."""
    # Create BannerConfig with all defaults
    banner_config = BannerConfig()
    
    # Update with parsed configuration
    for key, value in config_dict.items():
        if hasattr(banner_config, key):
            setattr(banner_config, key, value)
    
    return banner_config

def get_banner_config_from_cli(args=None):
    """Main function to get BannerConfig from new CLI system."""
    config_dict = parse_new_cli_arguments(args)
    return convert_to_banner_config(config_dict)

# Backward compatibility function
def get_args_from_new_cli(args=None):
    """Get arguments in old format for backward compatibility."""
    config_dict = parse_new_cli_arguments(args)
    
    # Create a simple namespace object with the configuration
    class Args:
        pass
    
    args_obj = Args()
    for key, value in config_dict.items():
        setattr(args_obj, key, value)
    
    return args_obj