"""
Stars motif - filled stars pattern
"""
from ._utils import fill_area_2d
from PIL import ImageDraw

def motif_star(draw, cx, cy, size, color, rot, fill_type, SS=1, **kwargs):
    from math import sin, cos, pi
    r_outer = size // 2
    r_inner = r_outer * 0.5
    points = []
    for i in range(10):
        angle = pi/2 + i * pi/5 + (rot * pi/180)
        r = r_outer if i % 2 == 0 else r_inner
        points.append((cx + r * cos(angle), cy - r * sin(angle)))
    if fill_type == 'filled':
        draw.polygon(points, fill=color)
    else:
        # Draw outline using line segments for better continuity
        line_width = max(2, 2*SS)
        for i in range(len(points)):
            start = points[i]
            end = points[(i + 1) % len(points)]
            draw.line([start, end], fill=color, width=line_width)

def apply_stars(grad, bg_box, H, density, opacity, jitter=0.0, size_variance=0.0, rotation=0, tilt=0, colors=None, SS=1):
    """Stars = filled stars"""
    W, H_img = grad.size
    density = max(density if density is not None else 1.0, 0.05)
    min_cell = max(8*SS, H//128, 24)
    cell = max(int(H * 0.10 / density) * SS, min_cell)
    cell = min(cell, H//2)
    
    # Stars are always filled
    fill_type = 'filled'
    
    grid_params = dict(cell=cell, jitter=int(cell*jitter), size_variance=size_variance, rotation=tilt, colors=colors, fill_type=fill_type, opacity=opacity, density=density)
    motif_params = {'SS': SS}
    return fill_area_2d(motif_star, grad, grid_params, motif_params)

def apply_stars_outline(grad, bg_box, H, density, opacity, jitter=0.0, size_variance=0.0, rotation=0, tilt=0, colors=None, SS=1):
    """Stars outline = outline stars"""
    W, H_img = grad.size
    density = max(density if density is not None else 1.0, 0.05)
    min_cell = max(8*SS, H//128, 24)
    cell = max(int(H * 0.10 / density) * SS, min_cell)
    cell = min(cell, H//2)
    
    # Stars outline are always outline
    fill_type = 'outline'
    
    grid_params = dict(cell=cell, jitter=int(cell*jitter), size_variance=size_variance, rotation=tilt, colors=colors, fill_type=fill_type, opacity=opacity, density=density)
    motif_params = {'SS': SS}
    return fill_area_2d(motif_star, grad, grid_params, motif_params)