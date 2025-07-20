# Utility functions for motifs
import random
import numpy as np
from PIL import Image, ImageDraw
from core.color_utils import parse_color, get_random_rotation

def fill_area_2d(draw_func, image, grid_params, motif_params):
    W, H = image.size
    cell = grid_params.get('cell', 32)
    if not isinstance(cell, int) or cell <= 0:
        raise ValueError(
            f"Motif grid cell parameter invalid! cell={cell}, density={grid_params.get('density', 'none')}, H={H}, grid_params={grid_params}"
        )
    jitter = grid_params.get('jitter', 0)
    size_variance = grid_params.get('size_variance', 0)
    rotation = grid_params.get('rotation', 0)
    colors = grid_params.get('colors')
    if not colors:
        colors = [(0,0,0,255)]  # Black for visibility on white background
    fill_type = grid_params.get('fill_type', 'filled')
    opacity = grid_params.get('opacity', 255)
    SS = motif_params.get('SS', 1)  # Get SS from motif_params
    draw = ImageDraw.Draw(image)
    for y in range(0, H, cell):
        for x in range(0, W, cell):
            cx = x + cell // 2 + (np.random.randint(-jitter, jitter) if jitter > 0 else 0)
            cy = y + cell // 2 + (np.random.randint(-jitter, jitter) if jitter > 0 else 0)
            base_size = max(8, int(cell * 0.6))  # Standard motifs - 60% of cell size
            size_var = max(1, int(base_size * size_variance))
            size = max(6, base_size + np.random.randint(-size_var, size_var))
            color = parse_color(random.choice(colors), opacity)
            shape_rot = get_random_rotation(rotation)
            # SS is already in motif_params, don't pass it separately
            draw_func(draw, cx, cy, size, color, shape_rot, fill_type, **motif_params)
    return image

def fill_area_1d(draw_func, image, line_params, motif_params):
    W, H = image.size
    colors = line_params.get('colors')
    opacity = line_params.get('opacity', 255)
    
    # Use colors array if provided, otherwise default to white
    if colors and len(colors) > 0:
        import random
        color = random.choice(colors)
    else:
        color = line_params.get('color') or (255,255,255,255)
    
    color = parse_color(color, opacity)
    width = line_params.get('width', 2)
    amp = line_params.get('amp', int(H*0.15))
    freq = line_params.get('freq', 2)
    step = line_params.get('step', int(W//16))
    spacing = line_params.get('spacing', width*3)
    spacing = max(spacing, 2)  # spacing should never be zero
    draw = ImageDraw.Draw(image)
    for y in range(spacing//2, H, spacing):
        draw_func(draw, (W, H), color, width=width, amp=amp, freq=freq, step=step, y_offset=y, **motif_params)
    return image

