"""
Lines motif - straight lines pattern
"""
from ._utils import fill_area_1d
from PIL import ImageDraw

def draw_line_straight(draw, size, color, width=2, amp=30, freq=2, step=8, y_offset=0, SS=1, **kwargs):
    W, H = size
    width = max(width, 2*SS)
    draw.line([0, y_offset, W, y_offset], fill=color, width=width)

def apply_lines(grad, bg_box, H, density, opacity, jitter=0.0, size_variance=0.0, rotation=0, tilt=0, colors=None, fill_type='filled', SS=1):
    """Lines = straight horizontal lines"""
    W, H_img = grad.size
    density = max(density if density is not None else 1.0, 0.05)
    
    # Line spacing based on density
    base_spacing = max(int(H * 0.08 / density) * SS, 8*SS)
    
    line_params = dict(
        colors=colors,
        opacity=opacity,
        width=max(2, 2*SS),  # Match 2D motif standard
        spacing=base_spacing,
        amp=0,  # No amplitude for straight lines
        freq=1,
        step=2
    )
    motif_params = {'SS': SS}
    return fill_area_1d(draw_line_straight, grad, line_params, motif_params)