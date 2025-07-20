"""
Hearts motif - filled hearts pattern
"""
from ._utils import fill_area_2d
from PIL import ImageDraw

def motif_heart(draw, cx, cy, size, color, rot, fill_type, SS=1, **kwargs):
    from math import sin, cos, pi, radians
    r = size // 2
    angle = radians(rot)
    points = []
    # Use smaller step for smoother heart curve
    for t in range(0, 360, 5):
        theta = pi * t / 180
        xh = r * 16 * sin(theta)**3
        yh = -r * (13 * cos(theta) - 5 * cos(2*theta) - 2 * cos(3*theta) - cos(4*theta))
        x_rot = xh * cos(angle) - yh * sin(angle)
        y_rot = xh * sin(angle) + yh * cos(angle)
        points.append((cx + x_rot/18, cy + y_rot/18))
    if fill_type == 'filled':
        draw.polygon(points, fill=color)
    else:
        # Draw outline using line segments for better continuity
        line_width = max(2, 2*SS)
        for i in range(len(points)):
            start = points[i]
            end = points[(i + 1) % len(points)]
            draw.line([start, end], fill=color, width=line_width)

def apply_hearts(grad, bg_box, H, density, opacity, jitter=0.0, size_variance=0.0, rotation=0, tilt=0, colors=None, SS=1):
    """Hearts = filled hearts"""
    W, H_img = grad.size
    density = max(density if density is not None else 1.0, 0.05)
    min_cell = max(8*SS, H//128, 24)
    cell = max(int(H * 0.10 / density) * SS, min_cell)
    cell = min(cell, H//2)
    
    # Hearts are always filled
    fill_type = 'filled'
    
    grid_params = dict(cell=cell, jitter=int(cell*jitter), size_variance=size_variance, rotation=tilt, colors=colors, fill_type=fill_type, opacity=opacity, density=density)
    motif_params = {'SS': SS}
    return fill_area_2d(motif_heart, grad, grid_params, motif_params)

def apply_hearts_outline(grad, bg_box, H, density, opacity, jitter=0.0, size_variance=0.0, rotation=0, tilt=0, colors=None, SS=1):
    """Hearts outline = outline hearts"""
    W, H_img = grad.size
    density = max(density if density is not None else 1.0, 0.05)
    min_cell = max(8*SS, H//128, 24)
    cell = max(int(H * 0.10 / density) * SS, min_cell)
    cell = min(cell, H//2)
    
    # Hearts outline are always outline
    fill_type = 'outline'
    
    grid_params = dict(cell=cell, jitter=int(cell*jitter), size_variance=size_variance, rotation=tilt, colors=colors, fill_type=fill_type, opacity=opacity, density=density)
    motif_params = {'SS': SS}
    return fill_area_2d(motif_heart, grad, grid_params, motif_params)