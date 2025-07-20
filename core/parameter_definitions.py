# parameter_definitions.py
"""
New CLI parameter definitions for compact multi-value system.
Defines clean, standardized parameter structure with help text.
"""

# Core Parameters (Simple, always present)
CORE_PARAMETERS = {
    'title': {
        'type': str,
        'default': 'Banner Maker',
        'help': 'Project title text'
    },
    'subtitle': {
        'type': str,
        'default': 'Customizable Project Banner Generator',
        'help': 'Project subtitle/description text'
    },
    'icon': {
        'type': str,
        'default': None,
        'help': 'Path to icon image file'
    },
    'output': {
        'type': str,
        'default': 'github_banner.png',
        'help': 'Output file name'
    },
    'preset': {
        'type': str,
        'default': None,
        'help': 'Use design preset (modern_blue, ocean_waves, etc.)'
    }
}

# Visual Design Parameters (Compact multi-value)
VISUAL_PARAMETERS = {
    'bg': {
        'type': str,
        'default': None,
        'help': 'Background colors and gradient type',
        'format': 'start:end:type',
        'examples': [
            'blue:purple:diagonal',
            '#ff0000:#00ff00:vertical',
            'red:orange:horizontal'
        ]
    },
    'text': {
        'type': str,
        'default': None,
        'help': 'Text color and shadow',
        'format': 'color:shadow',
        'examples': [
            'white:dark',
            '#ffffff:soft',
            'black:medium'
        ]
    },
    'accent': {
        'type': str,
        'default': None,
        'help': 'Accent color (auto-applies to shapes, patterns, highlights)',
        'format': 'color',
        'examples': [
            'blue',
            '#ff6b6b',
            'purple'
        ]
    }
}

# Design Element Parameters (Type:Config format)
ELEMENT_PARAMETERS = {
    'pattern': {
        'type': str,
        'default': None,
        'help': 'Background pattern/motif with advanced controls',
        'format': 'type:color:opacity:rotation:density:jitter',
        'examples': [
            'dots:white:30',
            'dots:white:100:45:1.5:0.3',
            'lines:gray:80:0:1.0:0.1',
            'triangles:blue:60:30:0.8:0.2'
        ]
    },
    'shape': {
        'type': str,
        'default': None,
        'help': 'Decorative shape element with parameters',
        'format': 'type:color:opacity:param1:param2',
        'examples': [
            'wave:blue:60',
            'wave:blue:60:2.5:0.4',
            'circle:red:80:50',
            'ellipse:green:70:80:40'
        ]
    },
    'texture': {
        'type': str,
        'default': None,
        'help': 'Background texture',
        'format': 'type:opacity',
        'examples': [
            'paper:20',
            'metal:30',
            'fabric:15'
        ]
    },
    'effect': {
        'type': str,
        'default': None,
        'help': 'Visual effect',
        'format': 'type:intensity',
        'examples': [
            'glow:soft',
            'shadow:medium',
            'blur:light'
        ]
    }
}

# Layout & Style Parameters (Standardized values)
STYLE_PARAMETERS = {
    'rounded': {
        'type': str,
        'default': None,
        'help': 'Corner radius (0-50)',
        'format': 'radius',
        'examples': ['20', '12', '0']
    },
    'padding': {
        'type': str,
        'default': None,
        'help': 'Internal spacing (20-60)',
        'format': 'pixels',
        'examples': ['32', '20', '50']
    },
    'size': {
        'type': str,
        'default': None,
        'help': 'Overall size scale',
        'format': 'scale',
        'examples': ['small', 'medium', 'large']
    }
}

# Smart Modifier Parameters
MODIFIER_PARAMETERS = {
    'intensity': {
        'type': str,
        'default': None,
        'help': 'Global intensity modifier (affects all opacity/contrast)',
        'format': 'level',
        'examples': ['low', 'medium', 'high']
    },
    'contrast': {
        'type': str,
        'default': None,
        'help': 'Global contrast modifier',
        'format': 'level',
        'examples': ['low', 'medium', 'high']
    },
    'test_element': {
        'type': str,
        'default': None,
        'help': 'Test specific element in isolation',
        'format': 'element_name',
        'examples': ['background', 'text', 'icon', 'pattern', 'shape', 'texture', 'effect']
    }
}

# All parameters combined
ALL_PARAMETERS = {
    **CORE_PARAMETERS,
    **VISUAL_PARAMETERS,
    **ELEMENT_PARAMETERS,
    **STYLE_PARAMETERS,
    **MODIFIER_PARAMETERS
}

def get_parameter_help():
    """Generate comprehensive help text for all parameters."""
    help_text = []
    
    help_text.append("GitHub Banner Maker - New CLI Parameter System")
    help_text.append("=" * 50)
    help_text.append("")
    
    # Core Parameters
    help_text.append("CORE PARAMETERS:")
    help_text.append("-" * 20)
    for name, info in CORE_PARAMETERS.items():
        help_text.append(f"  --{name}")
        help_text.append(f"    {info['help']}")
        if info['default']:
            help_text.append(f"    Default: {info['default']}")
        help_text.append("")
    
    # Visual Parameters
    help_text.append("VISUAL DESIGN PARAMETERS:")
    help_text.append("-" * 30)
    for name, info in VISUAL_PARAMETERS.items():
        help_text.append(f"  --{name} \"{info['format']}\"")
        help_text.append(f"    {info['help']}")
        if 'examples' in info:
            help_text.append(f"    Examples: {', '.join(info['examples'])}")
        help_text.append("")
    
    # Element Parameters
    help_text.append("DESIGN ELEMENT PARAMETERS:")
    help_text.append("-" * 30)
    for name, info in ELEMENT_PARAMETERS.items():
        help_text.append(f"  --{name} \"{info['format']}\"")
        help_text.append(f"    {info['help']}")
        if 'examples' in info:
            help_text.append(f"    Examples: {', '.join(info['examples'])}")
        help_text.append("")
    
    # Style Parameters
    help_text.append("STYLE PARAMETERS:")
    help_text.append("-" * 20)
    for name, info in STYLE_PARAMETERS.items():
        help_text.append(f"  --{name} \"{info['format']}\"")
        help_text.append(f"    {info['help']}")
        if 'examples' in info:
            help_text.append(f"    Examples: {', '.join(info['examples'])}")
        help_text.append("")
    
    # Modifier Parameters
    help_text.append("SMART MODIFIERS:")
    help_text.append("-" * 20)
    for name, info in MODIFIER_PARAMETERS.items():
        help_text.append(f"  --{name} \"{info['format']}\"")
        help_text.append(f"    {info['help']}")
        if 'examples' in info:
            help_text.append(f"    Examples: {', '.join(info['examples'])}")
        help_text.append("")
    
    # Usage Examples
    help_text.append("USAGE EXAMPLES:")
    help_text.append("-" * 20)
    help_text.append("  # Simple preset usage")
    help_text.append("  python banner_maker.py --preset modern_blue --title \"My Project\"")
    help_text.append("")
    help_text.append("  # Medium complexity")
    help_text.append("  python banner_maker.py --title \"API Docs\" --bg \"blue:purple:diagonal\" --pattern \"dots:white:30\"")
    help_text.append("")
    help_text.append("  # Full control")
    help_text.append("  python banner_maker.py --title \"My Project\" --bg \"orange:red:diagonal\" \\")
    help_text.append("                --pattern \"dots:white:25\" --shape \"wave:accent:60\" \\")
    help_text.append("                --accent \"blue\" --effect \"glow:soft\" --rounded \"20\"")
    help_text.append("")
    help_text.append("  # Smart modifiers")
    help_text.append("  python banner_maker.py --preset ocean_waves --title \"My Project\" --accent \"red\" --intensity \"high\"")
    help_text.append("")
    
    return "\n".join(help_text)

def get_parameter_short_help():
    """Generate concise help text for quick reference."""
    help_text = []
    
    help_text.append("Quick Reference:")
    help_text.append("  --preset NAME --title \"Text\"     # Use preset")
    help_text.append("  --bg \"start:end:type\"           # Background")
    help_text.append("  --text \"color:shadow\"           # Text styling")
    help_text.append("  --pattern \"type:color:opacity\"  # Background pattern")
    help_text.append("  --shape \"type:color:opacity\"    # Decorative shape")
    help_text.append("  --accent \"color\"                # Accent color")
    help_text.append("  --intensity \"low/medium/high\"   # Global intensity")
    help_text.append("  --rounded \"radius\"              # Corner radius")
    help_text.append("")
    help_text.append("Examples:")
    help_text.append("  python banner_maker.py --preset modern_blue --title \"My Project\"")
    help_text.append("  python banner_maker.py --title \"API\" --bg \"blue:purple:diagonal\" --pattern \"dots:white:30\"")
    help_text.append("")
    help_text.append("Use --help-full for detailed documentation.")
    
    return "\n".join(help_text)

# Available choices for validation
PARAMETER_CHOICES = {
    'gradient_type': ['vertical', 'horizontal', 'diagonal', 'radial'],
    'texture_type': ['paper', 'metal', 'fabric', 'wood', 'stone', 'noise', 'dots', 'lines'],
    'pattern_type': ['dots', 'lines', 'circles', 'squares', 'stars', 'triangles', 'hearts'],
    'shape_type': ['wave', 'circle', 'ellipse', 'rectangle', 'triangle'],
    'effect_type': ['glow', 'shadow', 'blur', 'lens_flare'],
    'intensity_level': ['low', 'medium', 'high'],
    'size_scale': ['small', 'medium', 'large'],
    'shadow_type': ['soft', 'medium', 'dark', 'true', 'false']
}

def validate_parameter_value(param_name, value):
    """Validate parameter value against allowed choices."""
    if param_name in PARAMETER_CHOICES:
        return value.lower() in PARAMETER_CHOICES[param_name]
    return True  # No validation needed for this parameter