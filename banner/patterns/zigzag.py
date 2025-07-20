"""
Zigzag motif - zigzag lines pattern
"""
from ._utils import fill_area_1d
from PIL import ImageDraw

def draw_line_zigzag(draw, size, color, width=2, amp=30, freq=2, step=8, y_offset=0, SS=1, **kwargs):
    W, H = size
    width = max(width, 2*SS)
    points = []
    zigzag_period = W // (freq * 2)
    for x in range(0, W, step):
        cycle_pos = (x % zigzag_period) / zigzag_period
        y = int(y_offset + amp * (1 - 2 * abs(cycle_pos - 0.5)))
        points.append((x, y))
    if len(points) > 1:
        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill=color, width=width)

def apply_zigzag(grad, bg_box, H, density, opacity, jitter=0.0, size_variance=0.0, rotation=0, tilt=0, colors=None, fill_type='filled', SS=1, freq=None, amp=None):
    """Zigzag = zigzag lines"""
    W, H_img = grad.size
    density = max(density if density is not None else 1.0, 0.05)
    
    # Line spacing based on density
    base_spacing = max(int(H * 0.12 / density) * SS, 12*SS)
    
    # Direct frequency and amplitude parameters
    # Default: freq=1.5, amp=25px (adjusted for visual consistency with sine/wave)
    freq = max(0.5, min(10, freq if freq is not None else 1.5))
    amp = max(5, min(50, amp if amp is not None else 25))
    
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
    return fill_area_1d(draw_line_zigzag, grad, line_params, motif_params)