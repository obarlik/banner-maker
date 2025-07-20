# constants.py
"""
Centralized constants for banner generation.
Eliminates magic numbers scattered throughout the codebase.
"""

# === BANNER DIMENSIONS ===
DEFAULT_BANNER_WIDTH = 1024
DEFAULT_BANNER_HEIGHT = 256
DEFAULT_ASPECT_RATIO = DEFAULT_BANNER_WIDTH / DEFAULT_BANNER_HEIGHT

# === SUPERSAMPLING ===
MIN_SUPERSAMPLING = 1
MAX_SUPERSAMPLING = 4
DEFAULT_SUPERSAMPLING = 2

# === COLORS ===
DEFAULT_BG_START = "#0052CC"
DEFAULT_BG_END = "#172B4D"
DEFAULT_TEXT_COLOR = "auto"
DEFAULT_BORDER_COLOR = "#c8c8c8"

# Color validation
MIN_RGB_VALUE = 0
MAX_RGB_VALUE = 255
MIN_OPACITY = 0
MAX_OPACITY = 255

# Default colors for various elements
DEFAULT_SHADOW_COLOR = (0, 0, 0)
DEFAULT_GLOW_COLOR = (255, 255, 255)
DEFAULT_TRANSPARENT = (0, 0, 0, 0)

# === OPACITY VALUES ===
OPACITY_TRANSPARENT = 0
OPACITY_SEMI_TRANSPARENT = 128
OPACITY_OPAQUE = 255

# Common opacity presets
OPACITY_SUBTLE = 64
OPACITY_MODERATE = 128
OPACITY_STRONG = 192

# === FONT SETTINGS ===
DEFAULT_TITLE_FONT = "DejaVuSansMono-Bold.ttf"
DEFAULT_SUBTITLE_FONT = "DejaVuSansMono.ttf"

# Font size limits
MIN_FONT_SIZE = 8
MAX_FONT_SIZE = 200
DEFAULT_MIN_FONT_SIZE = 12

# Font scaling factors
SUBTITLE_SCALE_FACTOR = 0.45
LINE_HEIGHT_FACTOR = 1.2

# === ICON SETTINGS ===
DEFAULT_ICON_SIZE = 120
MIN_ICON_SIZE = 16
MAX_ICON_SIZE = 512

ICON_POSITION_RIGHT = "right"
ICON_POSITION_LEFT = "left"

# === BORDER AND RADIUS ===
DEFAULT_BORDER_WIDTH = 4
MIN_BORDER_WIDTH = 1
MAX_BORDER_WIDTH = 20

DEFAULT_CORNER_RADIUS = 0
MIN_CORNER_RADIUS = 0
MAX_CORNER_RADIUS = 50

# Radius calculation factor
CORNER_RADIUS_HEIGHT_FACTOR = 6  # height // 6

# === PADDING AND SPACING ===
DEFAULT_PADDING = 32
MIN_PADDING = 0
MAX_PADDING = 100

DEFAULT_TEXT_BOX_PADDING = 12
DEFAULT_TEXT_BOX_RADIUS = 8

# === TEXTURE SETTINGS ===
TEXTURE_NONE = "none"

# Texture density limits
MIN_TEXTURE_DENSITY = 0.1
MAX_TEXTURE_DENSITY = 2.0
DEFAULT_TEXTURE_DENSITY = 1.0

# Texture displacement and shading
DEFAULT_DISPLACEMENT_STRENGTH = 12.0
DEFAULT_SHADING_STRENGTH = 4.0
DEFAULT_TEXTURE_SCALE = 1.0
DEFAULT_TEXTURE_CONTRAST_BOOST = 1.0
DEFAULT_TEXTURE_BLUR = 0.0
DEFAULT_TEXTURE_SEED = 42

# === MOTIF SETTINGS ===
MOTIF_NONE = "none"

# Motif parameters
MIN_MOTIF_JITTER = 0.0
MAX_MOTIF_JITTER = 1.0
DEFAULT_MOTIF_JITTER = 0.0

MIN_MOTIF_SIZE_VARIANCE = 0.0
MAX_MOTIF_SIZE_VARIANCE = 1.0
DEFAULT_MOTIF_SIZE_VARIANCE = 0.0

# Grid settings
DEFAULT_GRID_SPACING = 80
MIN_GRID_SPACING = 20
MAX_GRID_SPACING = 200

# === GRADIENT TYPES ===
GRADIENT_VERTICAL = "vertical"
GRADIENT_HORIZONTAL = "horizontal"
GRADIENT_DIAGONAL = "diagonal"
GRADIENT_RADIAL = "radial"

DEFAULT_GRADIENT_TYPE = GRADIENT_VERTICAL

# === BLEND MODES ===
BLEND_NORMAL = "normal"
BLEND_MULTIPLY = "multiply"
BLEND_SCREEN = "screen"
BLEND_OVERLAY = "overlay"

# === NOISE AND EFFECTS ===
DEFAULT_NOISE_INTENSITY = 16
DEFAULT_GRAIN_INTENSITY = 10

# Shadow settings
DEFAULT_SHADOW_OPACITY = 100
DEFAULT_SHADOW_OFFSET = (2, 2)
DEFAULT_SHADOW_BLUR = 4

# Glow settings
DEFAULT_GLOW_RADIUS = 10
DEFAULT_GLOW_INTENSITY = 0.5

# === CONTRAST AND ACCESSIBILITY ===
MIN_CONTRAST_RATIO = 1.0
DEFAULT_MIN_CONTRAST_RATIO = 4.5
HIGH_CONTRAST_RATIO = 7.0

# Luminance thresholds
DARK_THRESHOLD = 128
LIGHT_THRESHOLD = 200

# === FILE FORMATS ===
FORMAT_PNG = "png"
FORMAT_JPG = "jpg"
FORMAT_JPEG = "jpeg"

DEFAULT_OUTPUT_FORMAT = FORMAT_PNG
DEFAULT_OUTPUT_FILENAME = "github_banner.png"

# Image quality settings
DEFAULT_JPEG_QUALITY = 90
MAX_JPEG_QUALITY = 100

# === ANIMATION AND TIMING ===
DEFAULT_FRAME_DURATION = 100  # milliseconds
MIN_FRAME_DURATION = 50
MAX_FRAME_DURATION = 2000

# === MATHEMATICAL CONSTANTS ===
GOLDEN_RATIO = 1.618033988749
PI = 3.141592653589793
TWO_PI = 2 * PI

# Common angles in degrees
ANGLE_90 = 90
ANGLE_180 = 180
ANGLE_270 = 270
ANGLE_360 = 360

# === VALIDATION LIMITS ===
MAX_TEXT_LENGTH = 1000
MAX_FILENAME_LENGTH = 255

# Performance limits
MAX_PROCESSING_WIDTH = 4096
MAX_PROCESSING_HEIGHT = 2048

# === ERROR CODES ===
class ErrorCodes:
    SUCCESS = 0
    INVALID_CONFIG = 1
    FONT_LOAD_ERROR = 2
    IMAGE_LOAD_ERROR = 3
    FILE_WRITE_ERROR = 4
    VALIDATION_ERROR = 5
    PROCESSING_ERROR = 6

# === LAYER TYPES ===
class LayerTypes:
    BACKGROUND = "background"
    SHAPE = "shape"
    MOTIF = "motif"
    ICON = "icon"
    TEXT = "text"
    TEXTURE = "texture"
    EFFECTS = "effects"
    OVERLAY = "overlay"
    MASK = "mask"
    BORDER = "border"

# === PRESET CATEGORIES ===
class PresetCategories:
    PROFESSIONAL = "professional"
    CREATIVE = "creative"
    MINIMAL = "minimal"
    COLORFUL = "colorful"
    DARK = "dark"
    LIGHT = "light"
    ACCESSIBLE = "accessible"

# === SHAPE TYPES ===
class ShapeTypes:
    NONE = "none"
    CIRCLE = "circle"
    RECTANGLE = "rectangle"
    TRIANGLE = "triangle"
    STAR = "star"
    POLYGON = "polygon"
    WAVE = "wave"

# === TEXTURE TYPES ===
class TextureTypes:
    NONE = "none"
    NOISE = "noise"
    GRAIN = "grain"
    CONCRETE = "concrete"

# === MOTIF TYPES ===
class MotifTypes:
    NONE = "none"
    DOTS = "dots"
    LINES = "lines"
    CIRCLES = "circles"
    SQUARES = "squares"
    STARS = "stars"
    TRIANGLES = "triangles"
    HEARTS = "hearts"
    SINE = "sine"
    ZIGZAG = "zigzag"
    ASCII_GRID = "ascii_grid"

# === POSITION CONSTANTS ===
class Positions:
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    TOP = "top"
    BOTTOM = "bottom"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"

# === ALGORITHM PARAMETERS ===
# Noise generation
NOISE_OCTAVES = 4
NOISE_PERSISTENCE = 0.5
NOISE_SCALE = 0.1

# Geometry calculations
BEZIER_PRECISION = 100
CURVE_SMOOTHNESS = 0.5

# Optimization
CACHE_SIZE_LIMIT = 100
MEMORY_LIMIT_MB = 512

# === PLATFORM DEFAULTS ===
class PlatformDefaults:
    WINDOWS_DPI = 96
    MAC_DPI = 72
    LINUX_DPI = 96
    
    DEFAULT_DPI = 72

# === DEVELOPMENT FLAGS ===
class DevFlags:
    DEBUG_MODE = False
    VERBOSE_LOGGING = False
    SAVE_INTERMEDIATE_STEPS = False
    PERFORMANCE_PROFILING = False

# === QUALITY PRESETS ===
class QualityPresets:
    DRAFT = {
        'supersampling': 1,
        'blur_quality': 'low',
        'texture_quality': 'low'
    }
    NORMAL = {
        'supersampling': 2,
        'blur_quality': 'medium',
        'texture_quality': 'medium'
    }
    HIGH = {
        'supersampling': 4,
        'blur_quality': 'high',
        'texture_quality': 'high'
    }

# === COMPATIBILITY ===
MINIMUM_PIL_VERSION = "9.0.0"
MINIMUM_NUMPY_VERSION = "1.20.0"
MINIMUM_PYTHON_VERSION = (3, 8)

# === RESOURCE LIMITS ===
MAX_MEMORY_USAGE_MB = 1024
MAX_PROCESSING_TIME_SECONDS = 300
MAX_CACHE_ENTRIES = 1000

# === STRING CONSTANTS ===
class Messages:
    FONT_LOAD_WARNING = "[WARN] Font could not be loaded: {font} ({error}), using default font."
    SCIPY_NOT_AVAILABLE = "Warning: scipy/matplotlib not available, advanced textures will be disabled"
    BANNER_SAVED = "Banner saved as {filename}"
    DEBUG_PROCESSING = "[DEBUG] Processing {layer} layer"
    CONFIG_VALIDATION_ERROR = "[ERROR] Configuration validation failed: {errors}"

# === VALID CHOICES FOR CLI ===
VALID_GRADIENTS = [GRADIENT_VERTICAL, GRADIENT_HORIZONTAL, GRADIENT_DIAGONAL, GRADIENT_RADIAL]

# Auto-generate valid lists from maps - no hardcoding!
def get_valid_textures():
    """Get valid texture names from TEXTURE_MAP"""
    valid = ["none"]
    try:
        from banner.textures import TEXTURE_MAP
        valid.extend(TEXTURE_MAP.keys())
    except ImportError:
        pass
    return valid

def get_valid_patterns():
    """Get valid pattern names from PATTERN_MAP"""
    valid = ["none"]
    try:
        from banner.patterns import PATTERN_MAP
        valid.extend(PATTERN_MAP.keys())
    except ImportError:
        pass
    return valid

def get_valid_shapes():
    """Get valid shape names from SHAPE_MAP"""
    valid = ["none"]
    try:
        from banner.shapes import SHAPE_MAP
        valid.extend(SHAPE_MAP.keys())
    except ImportError:
        pass
    return valid

def get_valid_effects():
    """Get valid effect names from EFFECT_MAP"""
    valid = ["none"]
    try:
        from banner.effects import EFFECT_MAP
        valid.extend(EFFECT_MAP.keys())
    except ImportError:
        pass
    return valid

# Auto-generate lists (backwards compatibility)
VALID_TEXTURES = get_valid_textures()
VALID_PATTERNS = get_valid_patterns()
VALID_SHAPES = get_valid_shapes()
VALID_EFFECTS = get_valid_effects()

VALID_POSITIONS = [
    "left", "right", "center", "top", "bottom", "top_left", "top_right", 
    "bottom_left", "bottom_right", "custom"
]

VALID_INTENSITIES = ["low", "medium", "high"]
VALID_SIZES = ["small", "medium", "large"]
VALID_SHADOW_TYPES = ["soft", "medium", "dark", "true", "false"]

# === REGEX PATTERNS ===
HEX_COLOR_PATTERN = r'^#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$'
RGBA_PATTERN = r'^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([01]?\.?\d*))?\s*\)$'
FILENAME_SAFE_PATTERN = r'^[a-zA-Z0-9_\-\.]+$'