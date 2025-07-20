# geometry_utils.py
"""
Centralized geometry and gradient utilities for banner generation.
Consolidates geometric calculations and gradient functions.
"""

from PIL import Image, ImageDraw
import math
from .color_utils import interpolate_color


def draw_asym_rounded_rectangle(draw, box, radii, fill=None, outline=None, width=1, SS=1):
    """
    Draw asymmetric rounded rectangle with different corner radii.
    Consolidated version from background.py and image_utils.py.
    """
    x0, y0, x1, y1 = box
    tl, tr, br, bl = [r * SS for r in radii]
    
    # Ensure radii don't exceed box dimensions
    max_w = (x1 - x0) // 2
    max_h = (y1 - y0) // 2
    tl = min(tl, max_w, max_h)
    tr = min(tr, max_w, max_h)
    br = min(br, max_w, max_h)
    bl = min(bl, max_w, max_h)
    
    # Draw corner arcs
    if tl > 0:
        draw.pieslice([x0, y0, x0+2*tl, y0+2*tl], 180, 270, fill=fill)
    if tr > 0:
        draw.pieslice([x1-2*tr, y0, x1, y0+2*tr], 270, 360, fill=fill)
    if br > 0:
        draw.pieslice([x1-2*br, y1-2*br, x1, y1], 0, 90, fill=fill)
    if bl > 0:
        draw.pieslice([x0, y1-2*bl, x0+2*bl, y1], 90, 180, fill=fill)
    
    # Draw connecting rectangles
    draw.rectangle([x0+tl, y0, x1-tr, y0+max(tl,tr)], fill=fill)
    draw.rectangle([x0, y0+tl, x0+max(tl,bl), y1-bl], fill=fill)
    draw.rectangle([x1-max(tr,br), y0+tr, x1, y1-br], fill=fill)
    draw.rectangle([x0+bl, y1-max(bl,br), x1-br, y1], fill=fill)
    draw.rectangle([x0+tl, y0+max(tl,tr), x1-tr, y1-max(bl,br)], fill=fill)
    
    if outline and width > 0:
        # Draw outline (simplified for now)
        draw.rectangle(box, outline=outline, width=width)


def gradient_vertical(img, box, start, end):
    """Draw vertical gradient in specified box."""
    draw = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    h = y1 - y0 + 1
    for y in range(y0, y1 + 1):
        ratio = (y - y0) / max(1, h - 1)
        color = interpolate_color(start, end, ratio)
        draw.line([(x0, y), (x1, y)], fill=color + (255,))


def gradient_horizontal(img, box, start, end):
    """Draw horizontal gradient in specified box."""
    draw = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    w = x1 - x0 + 1
    for x in range(x0, x1 + 1):
        ratio = (x - x0) / max(1, w - 1)
        color = interpolate_color(start, end, ratio)
        draw.line([(x, y0), (x, y1)], fill=color + (255,))


def gradient_diagonal(img, box, start, end):
    """Draw diagonal gradient in specified box."""
    draw = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    w, h = x1 - x0 + 1, y1 - y0 + 1
    max_dist = max(w, h)
    
    for i in range(max_dist):
        ratio = i / max(1, max_dist - 1)
        color = interpolate_color(start, end, ratio)
        x = int(x0 + i * w / max_dist)
        y = int(y0 + i * h / max_dist)
        if x <= x1 and y <= y1:
            draw.line([(x0, y), (x, y1)], fill=color + (255,))


def gradient_radial(img, box, start, end):
    """Draw radial gradient in specified box."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0 + 1, y1 - y0 + 1
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    max_radius = ((w / 2) ** 2 + (h / 2) ** 2) ** 0.5
    
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            ratio = min(1, dist / max_radius)
            color = interpolate_color(start, end, ratio)
            img.putpixel((x, y), color + (255,))


def gradient_none(img, box, start, end):
    """Solid color fill - no gradient."""
    draw = ImageDraw.Draw(img)
    draw.rectangle(box, fill=start + (255,))


# Gradient function mapping
GRADIENT_MAP = {
    "vertical": gradient_vertical,
    "horizontal": gradient_horizontal,
    "diagonal": gradient_diagonal,
    "radial": gradient_radial,
    "none": gradient_none,
}


def draw_gradient_custom(img, box, start, end, grad_type="vertical"):
    """Draw gradient with specified type."""
    func = GRADIENT_MAP.get(grad_type, gradient_vertical)
    func(img, box, start, end)


def draw_simple_gradient(draw, width, height, start, end):
    """Simple vertical gradient drawing."""
    for y in range(height):
        ratio = y / max(1, height - 1)
        color = interpolate_color(start, end, ratio)
        draw.line([(0, y), (width, y)], fill=color)


def calculate_wave_points(width, height, amplitude, frequency, phase=0):
    """Calculate points for wave shape."""
    points = []
    for x in range(width):
        y = height // 2 + amplitude * math.sin(2 * math.pi * frequency * x / width + phase)
        points.append((x, int(y)))
    return points


def calculate_sine_wave(width, height, amp, freq, step=2, y_offset=None):
    """Calculate sine wave points."""
    y_center = y_offset if y_offset is not None else height // 2
    points = []
    for x in range(0, width, step):
        y = y_center + amp * math.sin(2 * math.pi * freq * x / width)
        points.append((x, int(y)))
    return points


def calculate_triangle_points(center_x, center_y, size, rotation=0):
    """Calculate triangle points with rotation."""
    # Equilateral triangle
    height = size * math.sqrt(3) / 2
    points = [
        (center_x, center_y - height * 2/3),  # Top
        (center_x - size/2, center_y + height * 1/3),  # Bottom left
        (center_x + size/2, center_y + height * 1/3),  # Bottom right
    ]
    
    if rotation != 0:
        # Rotate points around center
        cos_r = math.cos(math.radians(rotation))
        sin_r = math.sin(math.radians(rotation))
        rotated_points = []
        for x, y in points:
            # Translate to origin, rotate, translate back
            rel_x, rel_y = x - center_x, y - center_y
            new_x = rel_x * cos_r - rel_y * sin_r + center_x
            new_y = rel_x * sin_r + rel_y * cos_r + center_y
            rotated_points.append((new_x, new_y))
        return rotated_points
    
    return points


def calculate_star_points(center_x, center_y, size, points=5, rotation=0):
    """Calculate star points with specified number of points."""
    outer_radius = size // 2
    inner_radius = outer_radius * 0.4
    angle_step = 360 / (points * 2)
    
    star_points = []
    for i in range(points * 2):
        angle = math.radians(i * angle_step + rotation)
        radius = outer_radius if i % 2 == 0 else inner_radius
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        star_points.append((x, y))
    
    return star_points


def calculate_polygon_points(center_x, center_y, size, sides, rotation=0):
    """Calculate regular polygon points."""
    radius = size // 2
    angle_step = 360 / sides
    points = []
    
    for i in range(sides):
        angle = math.radians(i * angle_step + rotation)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    
    return points


def point_in_triangle(p, a, b, c):
    """Check if point p is inside triangle abc using barycentric coordinates."""
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    
    d1 = sign(p, a, b)
    d2 = sign(p, b, c)
    d3 = sign(p, c, a)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (has_neg and has_pos)


def distance_to_line(point, line_start, line_end):
    """Calculate distance from point to line segment."""
    x0, y0 = point
    x1, y1 = line_start
    x2, y2 = line_end
    
    # Line equation: Ax + By + C = 0
    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2
    
    # Distance formula
    return abs(A * x0 + B * y0 + C) / math.sqrt(A * A + B * B + 1e-8)


def normalize_angle(angle):
    """Normalize angle to 0-360 degrees."""
    return angle % 360


def scale_point(point, factor, center=(0, 0)):
    """Scale point around center."""
    x, y = point
    cx, cy = center
    return (
        cx + (x - cx) * factor,
        cy + (y - cy) * factor
    )


def rotate_point(point, angle, center=(0, 0)):
    """Rotate point around center."""
    x, y = point
    cx, cy = center
    cos_a = math.cos(math.radians(angle))
    sin_a = math.sin(math.radians(angle))
    
    # Translate to origin, rotate, translate back
    rel_x, rel_y = x - cx, y - cy
    new_x = rel_x * cos_a - rel_y * sin_a + cx
    new_y = rel_x * sin_a + rel_y * cos_a + cy
    
    return (new_x, new_y)


def create_layer_mask(size, border_width=0, corner_radii=None, SS=1):
    """
    Create layer mask with border and corner radius support.
    Consolidated from effects.py and pipeline.py mask generation logic.
    
    Args:
        size: (width, height) tuple
        border_width: Border width in pixels
        corner_radii: Dict with 'tl', 'tr', 'bl', 'br' keys or single value
        SS: Supersampling factor
    """
    width, height = size
    mask = Image.new("L", (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    
    # Calculate box coordinates
    bg_box = [
        border_width * SS,
        border_width * SS,
        width - border_width * SS - 1,
        height - border_width * SS - 1
    ]
    
    # Handle corner radii
    if corner_radii is None:
        corner_radii = {'tl': 0, 'tr': 0, 'bl': 0, 'br': 0}
    elif isinstance(corner_radii, (int, float)):
        # Single radius for all corners
        r = corner_radii
        corner_radii = {'tl': r, 'tr': r, 'bl': r, 'br': r}
    elif isinstance(corner_radii, (list, tuple)):
        # [tl, tr, br, bl] format
        if len(corner_radii) >= 4:
            corner_radii = {
                'tl': corner_radii[0],
                'tr': corner_radii[1], 
                'br': corner_radii[2],
                'bl': corner_radii[3]
            }
        else:
            corner_radii = {'tl': 0, 'tr': 0, 'bl': 0, 'br': 0}
    
    # Scale radii by supersampling and ensure they fit
    max_radius_w = (width - 2 * border_width * SS) // 2
    max_radius_h = (height - 2 * border_width * SS) // 2
    max_radius = min(max_radius_w, max_radius_h)
    
    scaled_radii = {
        key: max(0, min(max_radius, int(radius * SS) - border_width * SS))
        for key, radius in corner_radii.items()
    }
    
    # Draw mask
    if any(r > 0 for r in scaled_radii.values()):
        # Use asymmetric rounded rectangle
        radii_tuple = (
            scaled_radii['tl'],
            scaled_radii['tr'], 
            scaled_radii['br'],
            scaled_radii['bl']
        )
        draw_asym_rounded_rectangle(mask_draw, bg_box, radii_tuple, fill=255, SS=1)
    else:
        # Simple rectangle
        mask_draw.rectangle(bg_box, fill=255)
    
    return mask


def create_border_mask(size, border_width, corner_radii=None, SS=1):
    """
    Create border-only mask (outline).
    
    Args:
        size: (width, height) tuple
        border_width: Border width in pixels
        corner_radii: Corner radii configuration
        SS: Supersampling factor
    """
    width, height = size
    
    # Create outer mask (full shape)
    outer_mask = create_layer_mask(size, 0, corner_radii, SS)
    
    # Create inner mask (shape minus border)
    inner_size = (
        max(1, width - 2 * border_width * SS),
        max(1, height - 2 * border_width * SS)
    )
    
    # Adjust corner radii for inner mask
    if corner_radii:
        inner_radii = {}
        for key, radius in corner_radii.items():
            inner_radii[key] = max(0, radius - border_width)
    else:
        inner_radii = None
    
    inner_mask = create_layer_mask(inner_size, 0, inner_radii, SS)
    
    # Create border mask by subtracting inner from outer
    border_mask = Image.new("L", (width, height), 0)
    border_mask.paste(outer_mask, (0, 0))
    
    # Paste inner mask (inverted) to subtract
    inner_x = border_width * SS
    inner_y = border_width * SS
    inner_inverted = Image.eval(inner_mask, lambda x: 255 - x)
    
    # Create composite
    temp = Image.new("L", (width, height), 255)
    temp.paste(inner_inverted, (inner_x, inner_y))
    
    # Multiply masks to get border only
    border_pixels = []
    outer_pixels = list(outer_mask.getdata())
    temp_pixels = list(temp.getdata())
    
    for o, t in zip(outer_pixels, temp_pixels):
        border_pixels.append(min(o, t))
    
    border_mask.putdata(border_pixels)
    return border_mask


def apply_mask_to_image(image, mask, mode='alpha'):
    """
    Apply mask to image with different modes.
    
    Args:
        image: PIL Image to mask
        mask: PIL Image (mode 'L') to use as mask
        mode: 'alpha' (transparency) or 'clip' (hard cutoff)
    """
    if image.size != mask.size:
        mask = mask.resize(image.size, Image.LANCZOS)
    
    if mode == 'alpha':
        # Apply as alpha channel
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        
        # Combine with existing alpha
        r, g, b, a = image.split()
        mask_data = list(mask.getdata())
        alpha_data = list(a.getdata())
        
        # Multiply alphas
        new_alpha_data = [
            int((m / 255) * (a / 255) * 255)
            for m, a in zip(mask_data, alpha_data)
        ]
        
        new_alpha = Image.new("L", mask.size)
        new_alpha.putdata(new_alpha_data)
        
        return Image.merge("RGBA", (r, g, b, new_alpha))
    
    elif mode == 'clip':
        # Hard cutoff based on mask
        result = Image.new("RGBA", image.size, (0, 0, 0, 0))
        result.paste(image, (0, 0), mask)
        return result
    
    else:
        raise ValueError(f"Unknown mask mode: {mode}")


def create_gradient_mask(size, direction='vertical', start_opacity=255, end_opacity=0, center=None):
    """
    Create gradient mask for smooth transitions.
    
    Args:
        size: (width, height) tuple
        direction: 'vertical', 'horizontal', 'radial'
        start_opacity: Starting opacity (0-255)
        end_opacity: Ending opacity (0-255)
        center: Center point for radial gradient (x, y)
    """
    width, height = size
    mask = Image.new("L", (width, height))
    
    if direction == 'vertical':
        for y in range(height):
            ratio = y / max(1, height - 1)
            opacity = int(start_opacity * (1 - ratio) + end_opacity * ratio)
            for x in range(width):
                mask.putpixel((x, y), opacity)
                
    elif direction == 'horizontal':
        for x in range(width):
            ratio = x / max(1, width - 1)
            opacity = int(start_opacity * (1 - ratio) + end_opacity * ratio)
            for y in range(height):
                mask.putpixel((x, y), opacity)
                
    elif direction == 'radial':
        if center is None:
            center = (width // 2, height // 2)
        
        cx, cy = center
        max_dist = max(
            math.sqrt(cx**2 + cy**2),
            math.sqrt((width - cx)**2 + cy**2),
            math.sqrt(cx**2 + (height - cy)**2),
            math.sqrt((width - cx)**2 + (height - cy)**2)
        )
        
        for y in range(height):
            for x in range(width):
                dist = math.sqrt((x - cx)**2 + (y - cy)**2)
                ratio = min(1, dist / max_dist)
                opacity = int(start_opacity * (1 - ratio) + end_opacity * ratio)
                mask.putpixel((x, y), opacity)
    
    return mask


def create_feathered_mask(size, feather_radius=10, corner_radii=None):
    """
    Create mask with feathered (soft) edges.
    
    Args:
        size: (width, height) tuple
        feather_radius: Feather blur radius
        corner_radii: Corner radii configuration
    """
    # Create base mask
    base_mask = create_layer_mask(size, 0, corner_radii, 1)
    
    # Blur removed - SuperSampling provides anti-aliasing for feathering
    # if feather_radius > 0:
    #     from PIL import ImageFilter
    #     feathered = base_mask.filter(ImageFilter.GaussianBlur(feather_radius))
    #     return feathered
    
    return base_mask