# font_utils.py
"""
Centralized font utilities for banner generation.
Consolidates font loading, sizing, and text measurement functions.
"""

import os
from PIL import ImageFont
import platform


def find_font_path(font_name):
    """
    Find font file path across different operating systems.
    Consolidated font finding logic.
    """
    if os.path.isfile(font_name):
        return font_name
    
    # Extract filename if full path provided
    if '/' in font_name or '\\' in font_name:
        font_name = os.path.basename(font_name)
    
    # Check local fonts directory first (development)
    local_font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts', font_name)
    if os.path.isfile(local_font_path):
        return local_font_path
    
    # Check package fonts directory (installed package)
    try:
        # Try importlib.resources first (Python 3.9+)
        try:
            from importlib import resources
            with resources.path('fonts', font_name) as font_path:
                if font_path.exists():
                    return str(font_path)
        except (ImportError, AttributeError):
            # Fallback to pkg_resources
            import pkg_resources
            package_font_path = pkg_resources.resource_filename('', f'fonts/{font_name}')
            if os.path.isfile(package_font_path):
                return package_font_path
    except (ImportError, FileNotFoundError, ModuleNotFoundError):
        pass
    
    # Check if fonts are in site-packages directory
    try:
        import sys
        for path in sys.path:
            if 'site-packages' in path:
                fonts_path = os.path.join(path, 'fonts', font_name)
                if os.path.isfile(fonts_path):
                    return fonts_path
    except:
        pass
    
    # System font directories by platform
    system = platform.system().lower()
    font_dirs = []
    
    if system == 'windows':
        font_dirs = [
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'Fonts'),
        ]
    elif system == 'darwin':  # macOS
        font_dirs = [
            '/System/Library/Fonts',
            '/Library/Fonts',
            os.path.expanduser('~/Library/Fonts'),
        ]
    else:  # Linux and others
        font_dirs = [
            '/usr/share/fonts',
            '/usr/local/share/fonts',
            os.path.expanduser('~/.fonts'),
            os.path.expanduser('~/.local/share/fonts'),
        ]
    
    # Search in system directories
    for font_dir in font_dirs:
        if os.path.exists(font_dir):
            font_path = os.path.join(font_dir, font_name)
            if os.path.isfile(font_path):
                return font_path
            
            # Also search in subdirectories
            for root, dirs, files in os.walk(font_dir):
                if font_name in files:
                    return os.path.join(root, font_name)
    
    # Common font name mappings
    font_mappings = {
        'arial.ttf': ['arial.ttf', 'Arial.ttf', 'arial.TTF'],
        'arialbd.ttf': ['arialbd.ttf', 'Arial Bold.ttf', 'Arial-Bold.ttf'],
        'helvetica': ['Helvetica.ttc', 'helvetica.ttf'],
        'times': ['times.ttf', 'Times.ttc', 'TimesNewRoman.ttf'],
        'courier': ['courier.ttf', 'CourierNew.ttf'],
    }
    
    if font_name.lower() in font_mappings:
        for alt_name in font_mappings[font_name.lower()]:
            for font_dir in font_dirs:
                if os.path.exists(font_dir):
                    alt_path = os.path.join(font_dir, alt_name)
                    if os.path.isfile(alt_path):
                        return alt_path
    
    return font_name  # Return original if not found


def load_font_safe(font_name, size, fallback_size=None):
    """
    Safely load font with error handling and fallback.
    Consolidated from text.py font loading patterns.
    """
    if fallback_size is None:
        fallback_size = size
    
    try:
        font_path = find_font_path(font_name)
        font = ImageFont.truetype(font_path, size)
        
        # Ensure font has size attribute
        if not hasattr(font, 'size'):
            font.size = size
        
        return font, True  # Success flag
        
    except Exception as e:
        print(f"[WARN] Font could not be loaded: {font_name} (size: {size}) - {e}, using default font.")
        
        try:
            # Try default font
            font = ImageFont.load_default()
            if not hasattr(font, 'size'):
                font.size = fallback_size
            return font, False  # Default font used
        except Exception:
            # Last resort - create minimal font object
            font = type('Font', (), {
                'size': fallback_size,
                'getsize': lambda self, text: (len(text) * fallback_size // 2, fallback_size),
                'getbbox': lambda self, text: (0, 0, len(text) * fallback_size // 2, fallback_size)
            })()
            return font, False


def get_font_metrics(font, text):
    """
    Get comprehensive font metrics for text.
    Handles different PIL versions and font types.
    """
    if hasattr(font, 'getbbox'):
        # Newer PIL versions
        try:
            bbox = font.getbbox(text)
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            ascent = -bbox[1]
            descent = bbox[3] - ascent
            return {
                'width': width,
                'height': height,
                'ascent': ascent,
                'descent': descent,
                'bbox': bbox
            }
        except Exception:
            pass
    
    if hasattr(font, 'getsize'):
        # Older PIL versions
        try:
            width, height = font.getsize(text)
            return {
                'width': width,
                'height': height,
                'ascent': height,
                'descent': 0,
                'bbox': (0, 0, width, height)
            }
        except Exception:
            pass
    
    # Fallback calculation
    font_size = getattr(font, 'size', 12)
    width = len(text) * font_size // 2
    height = font_size
    
    return {
        'width': width,
        'height': height,
        'ascent': height,
        'descent': 0,
        'bbox': (0, 0, width, height)
    }


def get_text_width(font, text):
    """Get text width, handling various PIL versions."""
    metrics = get_font_metrics(font, text)
    return metrics['width']


def get_text_height(font, text):
    """Get text height, handling various PIL versions."""
    metrics = get_font_metrics(font, text)
    return metrics['height']


def calculate_font_size_to_fit(text, max_width, max_height, font_name, min_size=8, max_size=200):
    """
    Calculate optimal font size to fit text within bounds.
    Binary search approach for efficiency.
    """
    low, high = min_size, max_size
    best_size = min_size
    
    while low <= high:
        mid = (low + high) // 2
        font, _ = load_font_safe(font_name, mid)
        metrics = get_font_metrics(font, text)
        
        if metrics['width'] <= max_width and metrics['height'] <= max_height:
            best_size = mid
            low = mid + 1
        else:
            high = mid - 1
    
    return best_size


def calculate_multiline_size(lines, font):
    """Calculate size needed for multiline text."""
    if not lines:
        return 0, 0
    
    max_width = 0
    total_height = 0
    line_height = get_text_height(font, "Ag")  # Use ascenders/descenders for line height
    
    for i, line in enumerate(lines):
        width = get_text_width(font, line)
        max_width = max(max_width, width)
        
        if i == 0:
            total_height += line_height
        else:
            total_height += int(line_height * 1.2)  # Line spacing
    
    return max_width, total_height


def wrap_text_to_width(text, font, max_width):
    """Wrap text to fit within specified width."""
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if get_text_width(font, test_line) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                # Single word is too long, break it
                lines.append(word)
    
    if current_line:
        lines.append(current_line)
    
    return lines


def get_default_fonts():
    """Get list of commonly available fonts by platform."""
    system = platform.system().lower()
    
    if system == 'windows':
        return {
            'sans': ['arial.ttf', 'calibri.ttf', 'segoeui.ttf'],
            'serif': ['times.ttf', 'georgia.ttf'],
            'mono': ['consola.ttf', 'cour.ttf'],
            'bold': ['arialbd.ttf', 'calibrib.ttf']
        }
    elif system == 'darwin':  # macOS
        return {
            'sans': ['Helvetica.ttc', 'Arial.ttf', 'SanFrancisco.ttf'],
            'serif': ['Times.ttc', 'Georgia.ttf'],
            'mono': ['Monaco.ttf', 'Courier.ttc'],
            'bold': ['Helvetica-Bold.ttc', 'Arial-Bold.ttf']
        }
    else:  # Linux
        return {
            'sans': ['DejaVuSans.ttf', 'liberation-sans.ttf', 'ubuntu.ttf'],
            'serif': ['DejaVuSerif.ttf', 'liberation-serif.ttf'],
            'mono': ['DejaVuSansMono.ttf', 'liberation-mono.ttf'],
            'bold': ['DejaVuSans-Bold.ttf', 'liberation-sans-bold.ttf']
        }


def find_best_font(preferred_fonts, fallback_category='sans'):
    """Find the best available font from a list of preferences."""
    # Try preferred fonts first
    for font in preferred_fonts:
        font_path = find_font_path(font)
        if os.path.isfile(font_path):
            return font
    
    # Try default fonts for category
    defaults = get_default_fonts()
    if fallback_category in defaults:
        for font in defaults[fallback_category]:
            font_path = find_font_path(font)
            if os.path.isfile(font_path):
                return font
    
    # Last resort - any available font
    for category_fonts in defaults.values():
        for font in category_fonts:
            font_path = find_font_path(font)
            if os.path.isfile(font_path):
                return font
    
    return None  # No fonts found


def validate_font_file(font_path):
    """Validate that a font file is readable and usable."""
    try:
        test_font = ImageFont.truetype(font_path, 12)
        # Try to use the font
        test_font.getsize("Test")
        return True
    except Exception:
        return False


class FontManager:
    """Font management helper class."""
    
    def __init__(self):
        self.font_cache = {}
        self.available_fonts = None
    
    def get_font(self, font_name, size):
        """Get font with caching."""
        cache_key = f"{font_name}_{size}"
        if cache_key not in self.font_cache:
            font, success = load_font_safe(font_name, size)
            self.font_cache[cache_key] = font
        return self.font_cache[cache_key]
    
    def clear_cache(self):
        """Clear font cache."""
        self.font_cache.clear()
    
    def scan_available_fonts(self):
        """Scan system for available fonts."""
        if self.available_fonts is not None:
            return self.available_fonts
        
        fonts = set()
        defaults = get_default_fonts()
        
        for category_fonts in defaults.values():
            for font in category_fonts:
                if find_font_path(font) != font:  # Found on system
                    fonts.add(font)
        
        self.available_fonts = sorted(list(fonts))
        return self.available_fonts


# Global font manager instance
font_manager = FontManager()