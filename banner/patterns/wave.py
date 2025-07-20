"""
Wave motif - parallel wave lines pattern (S-shaped)
"""
from ._utils import fill_area_1d
from PIL import ImageDraw

def draw_line_wave(draw, size, color, width=2, amp=30, freq=2, step=8, y_offset=0, SS=1, **kwargs):
    """Draw parallel wave lines - S-shaped pattern"""
    from math import sin, cos, pi
    W, H = size
    width = max(width, 2*SS)
    points = []
    
    # Create S-shaped wave pattern
    for x in range(0, W, step):
        # S-curve using sine with phase shift
        t = x / W
        y = int(y_offset + amp * sin(2 * pi * freq * t + pi/2))
        points.append((x, y))
    
    if len(points) > 1:
        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill=color, width=width)

def apply_wave(grad, bg_box, H, density, opacity, jitter=0.0, size_variance=0.0, rotation=0, tilt=0, colors=None, fill_type='filled', SS=1, freq=None, amp=None):
    """Wave = parallel wave lines (S-shaped)"""
    W, H_img = grad.size
    density = max(density if density is not None else 1.0, 0.05)
    
    # Line spacing based on density
    base_spacing = max(int(H * 0.12 / density) * SS, 12*SS)
    
    # Direct frequency and amplitude parameters
    # Default: freq=3, amp=20px (standardized for 1D pattern tests)
    freq = max(0.5, min(10, freq if freq is not None else 3.0))
    amp = max(5, min(50, amp if amp is not None else 20))
    
    line_params = dict(
        colors=colors,
        opacity=opacity,
        width=max(2, 2*SS),  # Match 2D motif standard
        spacing=base_spacing,
        amp=amp,  # Direct amplitude in pixels
        freq=freq,  # Direct frequency value
        step=4
    )
    motif_params = {'SS': SS}
    return fill_area_1d(draw_line_wave, grad, line_params, motif_params)