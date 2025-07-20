"""
ASCII Grid motif - grid lines pattern
"""
from ._utils import fill_area_2d
from PIL import ImageDraw

def motif_ascii_grid(draw, cx, cy, size, color, rot, fill_type, SS=1, **kwargs):
    from PIL import ImageFont
    s = size
    
    # Draw grid lines instead of filled rectangles
    half = s // 2
    quarter = s // 4
    
    # Draw grid pattern (+ shape)
    line_width = max(2, 2*SS)
    draw.line([cx-half, cy, cx+half, cy], fill=color, width=line_width)  # Horizontal line
    draw.line([cx, cy-half, cx, cy+half], fill=color, width=line_width)  # Vertical line

def apply_ascii_grid(grad, bg_box, H, density, opacity, jitter=0.0, size_variance=0.0, rotation=0, tilt=0, colors=None, fill_type='filled', SS=1):
    """ASCII Grid = grid lines forming + pattern"""
    W, H_img = grad.size
    density = max(density if density is not None else 1.0, 0.05)
    min_cell = max(8*SS, H//128, 24)
    cell = max(int(H * 0.12 / density) * SS, min_cell)
    cell = min(cell, H//2)
    
    # ASCII grid uses line drawing
    fill_type = 'outline'
    
    grid_params = dict(cell=cell, jitter=int(cell*jitter), size_variance=size_variance, rotation=tilt, colors=colors, fill_type=fill_type, opacity=opacity, density=density)
    motif_params = {'SS': SS}
    return fill_area_2d(motif_ascii_grid, grad, grid_params, motif_params)