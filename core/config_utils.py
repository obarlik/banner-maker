# config_utils.py
"""
Centralized configuration utilities for banner generation.
Consolidates parameter extraction and validation patterns.
"""

def get_config_param(config, param_name, default_value=None, param_type=None):
    """
    Unified parameter extraction with type validation.
    Replaces repetitive getattr(config, 'param', default) patterns.
    """
    value = getattr(config, param_name, default_value)
    
    if param_type and value is not None:
        try:
            if param_type == bool:
                return bool(value)
            elif param_type == int:
                return int(value)
            elif param_type == float:
                return float(value)
            elif param_type == str:
                return str(value)
            elif param_type == tuple and isinstance(value, (list, tuple)):
                return tuple(value)
        except (ValueError, TypeError):
            return default_value
    
    return value


def extract_prefixed_params(config, prefix):
    """
    Extract all parameters with specified prefix from config.
    Example: extract_prefixed_params(config, 'overlay_') returns dict of overlay params.
    """
    params = {}
    for key, value in config.__dict__.items():
        if key.startswith(prefix):
            param_name = key.replace(prefix, '')
            params[param_name] = value
    return params


def validate_numeric_range(value, min_val=None, max_val=None, default=None):
    """Validate numeric value is within specified range."""
    if value is None:
        return default
    
    try:
        num_val = float(value)
        if min_val is not None and num_val < min_val:
            return min_val
        if max_val is not None and num_val > max_val:
            return max_val
        return num_val
    except (ValueError, TypeError):
        return default


def validate_opacity(value, default=255):
    """Validate opacity value (0-255)."""
    return int(validate_numeric_range(value, 0, 255, default))


def validate_density(value, default=1.0):
    """Validate density value (0.1-2.0)."""
    return validate_numeric_range(value, 0.1, 2.0, default)


def validate_color_string(color, default="#000000"):
    """Validate color string format."""
    if not isinstance(color, str):
        return default
    
    if color.startswith('#') and len(color) in [4, 7, 9]:  # #RGB, #RRGGBB, #RRGGBBAA
        try:
            int(color[1:], 16)  # Validate hex
            return color
        except ValueError:
            return default
    
    return default


def get_supersampling_factor(config, default=1):
    """Get supersampling factor with validation."""
    ss = get_config_param(config, 'SuperSampling', default, int)
    return max(1, min(4, ss))  # Limit to reasonable range


def get_scaled_param(config, param_name, default_value, ss_factor=None):
    """Get parameter scaled by supersampling factor."""
    value = get_config_param(config, param_name, default_value, int)
    if ss_factor is None:
        ss_factor = get_supersampling_factor(config)
    
    if value is not None and ss_factor > 1:
        return value * ss_factor
    return value


def extract_corner_radii(config, default_radius=0):
    """Extract corner radius values with fallback logic."""
    base_radius = get_config_param(config, 'corner_radius', default_radius, int)
    rounded = get_config_param(config, 'rounded', False, bool)
    
    # If rounded is True but no specific radii, use base calculation
    if rounded and base_radius == 0:
        height = get_config_param(config, 'height', 256, int)
        base_radius = height // 6
    
    return {
        'tl': get_config_param(config, 'corner_radius_tl', base_radius, int),
        'tr': get_config_param(config, 'corner_radius_tr', base_radius, int),
        'bl': get_config_param(config, 'corner_radius_bl', base_radius, int),
        'br': get_config_param(config, 'corner_radius_br', base_radius, int),
    }


def get_box_coordinates(config):
    """Get standard box coordinates from config."""
    width = get_config_param(config, 'width', 1024, int)
    height = get_config_param(config, 'height', 256, int)
    return [0, 0, width - 1, height - 1]


def get_color_params(config):
    """Extract all color-related parameters."""
    return {
        'bg_color_start': get_config_param(config, 'bg_color_start', '#0052CC', str),
        'bg_color_end': get_config_param(config, 'bg_color_end', '#172B4D', str),
        'text_color': get_config_param(config, 'text_color', 'auto', str),
        'border_color': get_config_param(config, 'border_color', '#c8c8c8', str),
        'icon_bg_color': get_config_param(config, 'icon_bg_color', None, str),
    }


def get_text_params(config):
    """Extract all text-related parameters."""
    return {
        'title': get_config_param(config, 'title', 'Banner Maker', str),
        'subtitle': get_config_param(config, 'subtitle', 'Customizable Project Banner Generator', str),
        'title_font': get_config_param(config, 'title_font', 'fonts/Inter-Bold.ttf', str),
        'subtitle_font': get_config_param(config, 'subtitle_font', 'fonts/Inter-Regular.ttf', str),
        'title_font_size': get_config_param(config, 'title_font_size', None, int),
        'subtitle_font_size': get_config_param(config, 'subtitle_font_size', None, int),
        'text_color': get_config_param(config, 'text_color', 'auto', str),
        'shadow': get_config_param(config, 'shadow', False, bool),
        'shadow_opacity': validate_opacity(get_config_param(config, 'shadow_opacity', 100)),
    }


def get_border_params(config):
    """Extract all border-related parameters."""
    return {
        'border': get_config_param(config, 'border', False, bool),
        'border_width': get_config_param(config, 'border_width', 4, int),
        'border_color': get_config_param(config, 'border_color', '#c8c8c8', str),
        'rounded': get_config_param(config, 'rounded', False, bool),
        **extract_corner_radii(config)
    }


def get_icon_params(config):
    """Extract all icon-related parameters."""
    return {
        'icon_path': get_config_param(config, 'icon_path', None, str),
        'icon_size': get_config_param(config, 'icon_size', 120, int),
        'icon_position': get_config_param(config, 'icon_position', 'right', str),
        'icon_bg_color': get_config_param(config, 'icon_bg_color', None, str),
        'icon_shadow': get_config_param(config, 'icon_shadow', False, bool),
        'icon_outline': get_config_param(config, 'icon_outline', False, bool),
        'auto_color': get_config_param(config, 'auto_color', True, bool),
    }


def get_texture_params(config):
    """Extract all texture-related parameters."""
    return {
        'texture': get_config_param(config, 'texture', 'none', str),
        'texture_density': validate_density(get_config_param(config, 'texture_density', 1.0)),
        'texture_opacity': validate_opacity(get_config_param(config, 'texture_opacity', 255)),
        'texture_rotation': get_config_param(config, 'texture_rotation', 0),
        'texture_colors': get_config_param(config, 'texture_colors', None),
        'texture_scale': get_config_param(config, 'texture_scale', 1.0, float),
        'texture_displacement_strength': get_config_param(config, 'texture_displacement_strength', 12.0, float),
        'texture_shading_strength': get_config_param(config, 'texture_shading_strength', 4.0, float),
        'texture_contrast_boost': get_config_param(config, 'texture_contrast_boost', 1.0, float),
        'texture_blur': get_config_param(config, 'texture_blur', 0.0, float),
        'texture_seed': get_config_param(config, 'texture_seed', 42, int),
    }


def get_motif_params(config):
    """Extract all motif-related parameters."""
    return {
        'motif': get_config_param(config, 'motif', 'none', str),
        'motif_density': validate_density(get_config_param(config, 'motif_density', 1.0)),
        'motif_opacity': validate_opacity(get_config_param(config, 'motif_opacity', 255)),
        'motif_rotation': get_config_param(config, 'motif_rotation', 0),
        'motif_colors': get_config_param(config, 'motif_colors', None),
        'motif_jitter': validate_numeric_range(get_config_param(config, 'motif_jitter', 0.0), 0.0, 1.0, 0.0),
        'motif_size_variance': validate_numeric_range(get_config_param(config, 'motif_size_variance', 0.0), 0.0, 1.0, 0.0),
        'motif_filled': get_config_param(config, 'motif_filled', True, bool),
    }


def validate_config_completeness(config, required_params):
    """Validate that config has all required parameters."""
    missing = []
    for param in required_params:
        if not hasattr(config, param) or getattr(config, param) is None:
            missing.append(param)
    return missing


def merge_configs(base_config, override_config):
    """Merge two config objects, with override taking precedence."""
    merged = base_config.__class__()
    
    # Copy base config
    for key, value in base_config.__dict__.items():
        setattr(merged, key, value)
    
    # Override with new values
    for key, value in override_config.__dict__.items():
        if value is not None:
            setattr(merged, key, value)
    
    return merged


class ConfigValidator:
    """Configuration validation helper class."""
    
    def __init__(self, config):
        self.config = config
        self.errors = []
        self.warnings = []
    
    def validate_required(self, param_name, param_type=None):
        """Validate required parameter exists and has correct type."""
        if not hasattr(self.config, param_name):
            self.errors.append(f"Missing required parameter: {param_name}")
            return False
        
        value = getattr(self.config, param_name)
        if value is None:
            self.errors.append(f"Required parameter {param_name} is None")
            return False
        
        if param_type and not isinstance(value, param_type):
            self.errors.append(f"Parameter {param_name} should be {param_type.__name__}, got {type(value).__name__}")
            return False
        
        return True
    
    def validate_range(self, param_name, min_val=None, max_val=None):
        """Validate parameter is within specified range."""
        if hasattr(self.config, param_name):
            value = getattr(self.config, param_name)
            if value is not None:
                try:
                    num_val = float(value)
                    if min_val is not None and num_val < min_val:
                        self.warnings.append(f"Parameter {param_name} ({num_val}) is below minimum ({min_val})")
                    if max_val is not None and num_val > max_val:
                        self.warnings.append(f"Parameter {param_name} ({num_val}) is above maximum ({max_val})")
                except (ValueError, TypeError):
                    self.errors.append(f"Parameter {param_name} should be numeric")
    
    def validate_choice(self, param_name, valid_choices):
        """Validate parameter is in list of valid choices."""
        if hasattr(self.config, param_name):
            value = getattr(self.config, param_name)
            if value is not None and value not in valid_choices:
                self.errors.append(f"Parameter {param_name} ({value}) not in valid choices: {valid_choices}")
    
    def has_errors(self):
        """Check if validation found any errors."""
        return len(self.errors) > 0
    
    def get_report(self):
        """Get validation report."""
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'valid': len(self.errors) == 0
        }