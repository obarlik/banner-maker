# effects/lens_flare.py
# Lens flare effect generation

import numpy as np
from PIL import Image, ImageFilter
import math

def apply_lens_flare(img, position="top_right", scale=1.0, SS=1, custom_x=None, custom_y=None, 
                    core_color=(255, 255, 255), ghost_colors=None, intensity=1.0, 
                    spike_enabled=True, hexagon_enabled=True, blur_layers=3):
    """Apply lens flare effect - enhanced version matching reference quality with full customization."""
    arr = np.array(img).astype(np.float32)
    h, w = arr.shape[:2]
    
    # Scale with SuperSampling
    scale = scale * SS
    
    # Enhanced colors for 4 ghost system
    if ghost_colors is None:
        ghost_colors = [
            (255, 255, 200),  # Bright white-yellow ghost
            (255, 140, 60),   # Warm orange ghost
            (60, 180, 120),   # Green ghost  
            (180, 100, 200),  # Purple ghost
        ]
    
    # Calculate flare position - custom coordinates override preset positions
    if custom_x is not None and custom_y is not None:
        pos_x, pos_y = custom_x, custom_y
    else:
        position_map = {
            "top_left": (0.15, 0.15),
            "top_right": (0.85, 0.15), 
            "center": (0.5, 0.5),
            "bottom_left": (0.15, 0.85),
            "bottom_right": (0.85, 0.85)
        }
        pos_x, pos_y = position_map.get(position, (0.85, 0.15))
    
    flare_x, flare_y = int(w * pos_x), int(h * pos_y)
    center_x, center_y = w // 2, h // 2
    
    # Calculate vector from flare to center for lens elements
    vec_x = center_x - flare_x
    vec_y = center_y - flare_y
    vec_length = math.sqrt(vec_x**2 + vec_y**2)
    
    # Normalize vector
    if vec_length > 0:
        vec_x_norm = vec_x / vec_length
        vec_y_norm = vec_y / vec_length
    else:
        vec_x_norm = vec_y_norm = 0
    
    # Create flare elements directly on the array for better blending
    flare_arr = np.zeros_like(arr)
    
    # Anti-aliased core like real Photoshop - no hard edges
    y_indices, x_indices = np.ogrid[:h, :w]
    core_dist = np.sqrt((x_indices - flare_x)**2 + (y_indices - flare_y)**2)
    
    # Smooth core system - completely gradient-based (no masks)
    base_intensity = 250 * intensity  # Increased intensity for better visibility
    
    # 1. Bright white center - more intense and larger
    core_center = np.exp(-core_dist / (5 * scale)) * base_intensity
    flare_arr[:, :, 0] += core_center * 1.2
    flare_arr[:, :, 1] += core_center * 1.2  
    flare_arr[:, :, 2] += core_center * 1.2
    
    # 2. Orange-pink ring - warmer and more prominent
    warm_ring = np.exp(-core_dist / (15 * scale)) * (base_intensity * 0.8)
    flare_arr[:, :, 0] += warm_ring * 1.0  # Strong orange
    flare_arr[:, :, 1] += warm_ring * 0.6  # Warm orange
    flare_arr[:, :, 2] += warm_ring * 0.3  # Orange tint
    
    # 3. Large warm glow - more visible and warmer
    warm_glow = np.exp(-core_dist / (80 * scale)) * (base_intensity * 0.4)
    flare_arr[:, :, 0] += warm_glow * 0.8  # Warm glow
    flare_arr[:, :, 1] += warm_glow * 0.5  # Warm glow
    flare_arr[:, :, 2] += warm_glow * 0.2  # Warm glow
    
    # Enhanced 4-ghost system for more dramatic effect
    ghost_positions = [0.2, 0.4, 0.7, 0.9]  # More distributed ghosts
    ghost_sizes = [
        int(25*scale),   # Small bright ghost
        int(45*scale),   # Medium orange ghost
        int(75*scale),   # Large green ghost  
        int(100*scale),  # Outer purple ghost
    ]
    ghost_intensities = [1.0, 0.9, 0.8, 0.5]  # Strong intensities
    
    for i, t in enumerate(ghost_positions):
        if i < len(ghost_colors):
            ghost_x = int(flare_x + vec_x * t)
            ghost_y = int(flare_y + vec_y * t)
            ghost_size = ghost_sizes[i]
            ghost_color = ghost_colors[i]
            ghost_intensity = ghost_intensities[i]
            
            # Reference-style circular ghost with very prominent ring structure
            ghost_dist = np.sqrt((x_indices - ghost_x)**2 + (y_indices - ghost_y)**2)
            ghost_mask = ghost_dist < ghost_size
            
            # Enhanced ghost rendering with stronger effects
            if i == 0:  # Bright white-yellow ghost - intense center
                ghost_fade = np.exp(-ghost_dist / (ghost_size * 0.6)) * ghost_intensity * 150
            elif i == 1:  # Orange ghost - warm with strong ring
                ghost_fade = np.exp(-ghost_dist / (ghost_size * 0.8)) * ghost_intensity * 120
                ring_factor = np.exp(-abs(ghost_dist - ghost_size * 0.6) / (ghost_size * 0.15))
                ghost_fade += ring_factor * 50  # Strong ring
            elif i == 2:  # Green ghost - distinctive color
                ghost_fade = np.exp(-ghost_dist / (ghost_size * 0.9)) * ghost_intensity * 100
                ring_factor = np.exp(-abs(ghost_dist - ghost_size * 0.7) / (ghost_size * 0.2))
                ghost_fade += ring_factor * 35  # Medium ring
            else:  # Purple ghost - subtle outer glow
                ghost_fade = np.exp(-ghost_dist / (ghost_size * 1.0)) * ghost_intensity * 80
                outer_factor = np.exp(-abs(ghost_dist - ghost_size * 0.8) / (ghost_size * 0.3))
                ghost_fade += outer_factor * 25  # Visible outer ring
                
            ghost_fade = np.clip(ghost_fade, 0, 255)
            
            # Apply to all pixels (no masking for smooth edges)
            flare_arr[:, :, 0] += ghost_fade * ghost_color[0] / 255
            flare_arr[:, :, 1] += ghost_fade * ghost_color[1] / 255
            flare_arr[:, :, 2] += ghost_fade * ghost_color[2] / 255
    
    # Clip flare values
    flare_arr = np.clip(flare_arr, 0, 255)
    
    # Very soft blur layers like Photoshop - subtle and gradual
    flare_img = Image.fromarray(flare_arr.astype(np.uint8), mode="RGBA")
    
    if blur_layers >= 1:
        # Subtle light blur
        flare_light_blur = flare_img.filter(ImageFilter.GaussianBlur(radius=1.5))
        flare_light_arr = np.array(flare_light_blur).astype(np.float32)
    else:
        flare_light_arr = flare_arr
    
    if blur_layers >= 2:
        # Medium soft blur
        flare_medium_blur = flare_img.filter(ImageFilter.GaussianBlur(radius=6))
        flare_medium_arr = np.array(flare_medium_blur).astype(np.float32)
    else:
        flare_medium_arr = np.zeros_like(flare_arr)
    
    if blur_layers >= 3:
        # Wide but very subtle blur like Photoshop
        flare_heavy_blur = flare_img.filter(ImageFilter.GaussianBlur(radius=15))
        flare_heavy_arr = np.array(flare_heavy_blur).astype(np.float32)
    else:
        flare_heavy_arr = np.zeros_like(flare_arr)
    
    # Very subtle layer combination like Photoshop
    if blur_layers == 1:
        final_flare = flare_arr * 0.8 + flare_light_arr * 0.2
    elif blur_layers == 2:
        final_flare = flare_arr * 0.6 + flare_light_arr * 0.25 + flare_medium_arr * 0.15
    else:  # 3 or more - very subtle blend
        final_flare = (flare_arr * 0.5 + 
                       flare_light_arr * 0.25 + 
                       flare_medium_arr * 0.15 + 
                       flare_heavy_arr * 0.1)
    
    # Screen blend mode: result = 1 - (1-base)(1-flare)
    result = 255 - (255 - arr) * (255 - final_flare) / 255
    result = np.clip(result, 0, 255).astype(np.uint8)
    
    return Image.fromarray(result, mode="RGBA")