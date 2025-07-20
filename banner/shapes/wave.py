# shapes/wave.py
# Wave shape generation

from PIL import Image, ImageDraw
import math
from ._utils import create_shape_overlay, ensure_color_tuple, composite_shape

def apply_wave(img, W, H, SS, color=(0, 200, 255, 90), amplitude=0.18, frequency=2, blur=16, 
               phases=3, phase_shift=0.8, transparency_decay=0.7):
    amplitude = max(amplitude if amplitude is not None else 0.18, 0.01)
    frequency = max(frequency if frequency is not None else 2, 0.1)
    blur = max(blur if blur is not None else 16, 0)
    phases = max(phases if phases is not None else 3, 1)
    phase_shift = max(phase_shift if phase_shift is not None else 0.8, 0.1)
    transparency_decay = max(transparency_decay if transparency_decay is not None else 0.7, 0.3)
    
    color = ensure_color_tuple(color)
    
    # Create multiple wave layers with different phases
    overlay = create_shape_overlay(img)
    
    for phase in range(phases):
        # Calculate phase offset and transparency
        phase_offset = phase * phase_shift * math.pi
        opacity_factor = transparency_decay ** phase
        
        # Create wave layer
        wave_layer = create_shape_overlay(img)
        draw = ImageDraw.Draw(wave_layer)
        
        wave_height = int(H * amplitude * (1 - phase * 0.2))  # Slightly decrease amplitude for each layer
        points = []
        
        for x in range(W):
            # Multiple sine waves with different frequencies for more natural look
            primary_wave = math.sin(2 * math.pi * frequency * x / W + phase_offset)
            secondary_wave = 0.3 * math.sin(2 * math.pi * frequency * 2.3 * x / W + phase_offset * 1.5)
            tertiary_wave = 0.15 * math.sin(2 * math.pi * frequency * 0.7 * x / W + phase_offset * 0.8)
            
            combined_wave = primary_wave + secondary_wave + tertiary_wave
            y = int(H - wave_height * (1 + combined_wave))
            points.append((x, y))
        
        # Close bottom edge for filled wave
        points += [(W-1, H), (0, H)]
        
        # Apply transparency based on layer
        wave_color = (color[0], color[1], color[2], int(color[3] * opacity_factor))
        draw.polygon(points, fill=wave_color)
        
        # Composite this layer onto the main overlay
        overlay = Image.alpha_composite(overlay, wave_layer)
    
    return composite_shape(img, overlay)