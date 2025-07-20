"""
Squares motif - filled squares pattern
"""
from ._utils import fill_area_2d
from PIL import ImageDraw

def motif_square(draw, cx, cy, size, color, rot, fill_type, SS=1, **kwargs):
    from math import cos, sin, radians
    half = size // 2
    angle = radians(rot)
    corners = [(-half, -half), (half, -half), (half, half), (-half, half)]
    rotated = [(cx + x*cos(angle) - y*sin(angle), cy + x*sin(angle) + y*cos(angle)) for x, y in corners]
    if fill_type == 'filled':
        draw.polygon(rotated, fill=color)
    else:
        draw.polygon(rotated, outline=color, width=max(2, 2*SS))

def apply_squares(grad, bg_box, H, density, opacity, jitter=0.0, size_variance=0.0, rotation=0, tilt=0, colors=None, SS=1):
    """Squares = filled squares"""
    W, H_img = grad.size
    density = max(density if density is not None else 1.0, 0.05)
    min_cell = max(8*SS, H//128, 24)
    cell = max(int(H * 0.10 / density) * SS, min_cell)
    cell = min(cell, H//2)
    
    # Squares are always filled
    fill_type = 'filled'
    
    grid_params = dict(cell=cell, jitter=int(cell*jitter), size_variance=size_variance, rotation=tilt, colors=colors, fill_type=fill_type, opacity=opacity, density=density)
    motif_params = {'SS': SS}
    return fill_area_2d(motif_square, grad, grid_params, motif_params)

def apply_squares_outline(grad, bg_box, H, density, opacity, jitter=0.0, size_variance=0.0, rotation=0, tilt=0, colors=None, SS=1):
    """Squares outline = outline squares"""
    W, H_img = grad.size
    density = max(density if density is not None else 1.0, 0.05)
    min_cell = max(8*SS, H//128, 24)
    cell = max(int(H * 0.10 / density) * SS, min_cell)
    cell = min(cell, H//2)
    
    # Squares outline are always outline
    fill_type = 'outline'
    
    grid_params = dict(cell=cell, jitter=int(cell*jitter), size_variance=size_variance, rotation=tilt, colors=colors, fill_type=fill_type, opacity=opacity, density=density)
    motif_params = {'SS': SS}
    return fill_area_2d(motif_square, grad, grid_params, motif_params)