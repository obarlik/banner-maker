"""
Dots motif - filled and outline circles pattern
"""
from ._utils import fill_area_2d
from PIL import ImageDraw

def motif_dot(draw, cx, cy, size, color, rot, fill_type, SS=1, **kwargs):
    r = size // 2
    if fill_type == 'filled':
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    else:
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=max(2, 2*SS))

def apply_dots(grad, bg_box, H, density, opacity, jitter=0.0, size_variance=0.0, rotation=0, tilt=0, colors=None, SS=1):
    """Dots = filled circles"""
    W, H_img = grad.size
    density = max(density if density is not None else 1.0, 0.05)
    min_cell = max(8*SS, H//128, 24)
    cell = max(int(H * 0.10 / density) * SS, min_cell)
    cell = min(cell, H//2)
    
    # Dots are always filled
    fill_type = 'filled'
    
    grid_params = dict(cell=cell, jitter=int(cell*jitter), size_variance=size_variance, rotation=tilt, colors=colors, fill_type=fill_type, opacity=opacity, density=density)
    motif_params = {'SS': SS}
    return fill_area_2d(motif_dot, grad, grid_params, motif_params)

def apply_circles(grad, bg_box, H, density, opacity, jitter=0.0, size_variance=0.0, rotation=0, tilt=0, colors=None, SS=1):
    """Circles = outline circles"""
    W, H_img = grad.size
    density = max(density if density is not None else 1.0, 0.05)
    min_cell = max(8*SS, H//128, 24)
    cell = max(int(H * 0.10 / density) * SS, min_cell)
    cell = min(cell, H//2)
    
    # Circles are always outline
    fill_type = 'outline'
    
    grid_params = dict(cell=cell, jitter=int(cell*jitter), size_variance=size_variance, rotation=tilt, colors=colors, fill_type=fill_type, opacity=opacity, density=density)
    motif_params = {'SS': SS}
    return fill_area_2d(motif_dot, grad, grid_params, motif_params)