# layer_utils.py
"""
Centralized layer composition and image utilities for banner generation.
Consolidates image layer operations and composition patterns.
"""

from PIL import Image, ImageDraw, ImageFilter
import numpy as np


def create_layer(size, color=(0, 0, 0, 0)):
    """Create new transparent layer with specified size."""
    if isinstance(size, tuple):
        width, height = size
    else:
        width = height = size
    return Image.new("RGBA", (width, height), color)


def apply_layer_with_opacity(base_layer, overlay_layer, opacity=255):
    """Apply overlay layer to base with specified opacity."""
    if opacity >= 255:
        return Image.alpha_composite(base_layer, overlay_layer)
    
    # Create opacity mask
    if overlay_layer.mode != "RGBA":
        overlay_layer = overlay_layer.convert("RGBA")
    
    # Adjust alpha channel
    data = np.array(overlay_layer)
    data[:, :, 3] = (data[:, :, 3] * opacity / 255).astype(np.uint8)
    overlay_with_opacity = Image.fromarray(data, "RGBA")
    
    return Image.alpha_composite(base_layer, overlay_with_opacity)


def blend_layers(layer1, layer2, mode='normal', opacity=1.0):
    """Blend two layers with specified blend mode and opacity."""
    if layer1.size != layer2.size:
        layer2 = layer2.resize(layer1.size, Image.LANCZOS)
    
    if mode == 'normal':
        return Image.blend(layer1, layer2, opacity)
    elif mode == 'multiply':
        # Implement multiply blend mode
        arr1 = np.array(layer1).astype(float) / 255
        arr2 = np.array(layer2).astype(float) / 255
        result = (arr1 * arr2 * 255).astype(np.uint8)
        blended = Image.fromarray(result, layer1.mode)
        return Image.blend(layer1, blended, opacity)
    elif mode == 'screen':
        # Implement screen blend mode
        arr1 = np.array(layer1).astype(float) / 255
        arr2 = np.array(layer2).astype(float) / 255
        result = (1 - (1 - arr1) * (1 - arr2)) * 255
        blended = Image.fromarray(result.astype(np.uint8), layer1.mode)
        return Image.blend(layer1, blended, opacity)
    else:
        return Image.blend(layer1, layer2, opacity)


def apply_mask_to_layer(layer, mask):
    """Apply mask to layer."""
    if mask.mode != "L":
        mask = mask.convert("L")
    
    result = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    result.paste(layer, (0, 0), mask=mask)
    return result


def create_circular_mask(size, center=None, radius=None):
    """Create circular mask."""
    width, height = size if isinstance(size, tuple) else (size, size)
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    if center is None:
        center = (width // 2, height // 2)
    if radius is None:
        radius = min(width, height) // 2
    
    left = center[0] - radius
    top = center[1] - radius
    right = center[0] + radius
    bottom = center[1] + radius
    
    draw.ellipse([left, top, right, bottom], fill=255)
    return mask


def create_gradient_mask(size, direction='vertical', start_alpha=255, end_alpha=0):
    """Create gradient mask for smooth transitions."""
    width, height = size if isinstance(size, tuple) else (size, size)
    mask = Image.new("L", (width, height))
    
    if direction == 'vertical':
        for y in range(height):
            ratio = y / max(1, height - 1)
            alpha = int(start_alpha * (1 - ratio) + end_alpha * ratio)
            for x in range(width):
                mask.putpixel((x, y), alpha)
    elif direction == 'horizontal':
        for x in range(width):
            ratio = x / max(1, width - 1)
            alpha = int(start_alpha * (1 - ratio) + end_alpha * ratio)
            for y in range(height):
                mask.putpixel((x, y), alpha)
    elif direction == 'radial':
        center_x, center_y = width // 2, height // 2
        max_dist = max(width, height) // 2
        for y in range(height):
            for x in range(width):
                dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                ratio = min(1, dist / max_dist)
                alpha = int(start_alpha * (1 - ratio) + end_alpha * ratio)
                mask.putpixel((x, y), alpha)
    
    return mask


def apply_shadow_to_layer(layer, offset=(2, 2), blur_radius=4, shadow_color=(0, 0, 0), opacity=128):
    """Apply drop shadow to layer."""
    # Create shadow layer
    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    
    # Extract alpha channel for shadow shape
    if layer.mode == "RGBA":
        alpha = layer.split()[-1]
    else:
        alpha = Image.new("L", layer.size, 255)
    
    # Create shadow with specified color
    shadow_img = Image.new("RGBA", layer.size, shadow_color + (opacity,))
    shadow.paste(shadow_img, (0, 0), alpha)
    
    # Blur removed - SuperSampling provides anti-aliasing for shadows
    # if blur_radius > 0:
    #     shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # Create result with shadow offset
    result_size = (
        layer.size[0] + abs(offset[0]) + blur_radius * 2,
        layer.size[1] + abs(offset[1]) + blur_radius * 2
    )
    result = Image.new("RGBA", result_size, (0, 0, 0, 0))
    
    # Paste shadow
    shadow_pos = (
        blur_radius + max(0, offset[0]),
        blur_radius + max(0, offset[1])
    )
    result.paste(shadow, shadow_pos, shadow)
    
    # Paste original layer
    layer_pos = (
        blur_radius + max(0, -offset[0]),
        blur_radius + max(0, -offset[1])
    )
    result.paste(layer, layer_pos, layer)
    
    return result


def apply_glow_to_layer(layer, radius=10, color=(255, 255, 255), intensity=0.5):
    """Apply glow effect to layer."""
    # Extract alpha for glow shape
    if layer.mode == "RGBA":
        alpha = layer.split()[-1]
    else:
        alpha = Image.new("L", layer.size, 255)
    
    # Create glow
    glow_size = (
        layer.size[0] + radius * 4,
        layer.size[1] + radius * 4
    )
    glow = Image.new("RGBA", glow_size, (0, 0, 0, 0))
    
    # Create glow layers with different intensities
    for i in range(radius):
        glow_alpha = int(255 * intensity * (1 - i / radius))
        glow_color = color + (glow_alpha,)
        glow_layer = Image.new("RGBA", layer.size, glow_color)
        
        # Apply alpha shape
        glow_with_shape = Image.new("RGBA", layer.size, (0, 0, 0, 0))
        glow_with_shape.paste(glow_layer, (0, 0), alpha)
        
        # Blur removed - SuperSampling provides anti-aliasing for glow
        # if i > 0:
        #     glow_with_shape = glow_with_shape.filter(ImageFilter.GaussianBlur(i))
        
        offset = radius * 2
        glow.paste(glow_with_shape, (offset, offset), glow_with_shape)
    
    # Paste original layer on top
    glow.paste(layer, (radius * 2, radius * 2), layer)
    return glow


def apply_border_to_layer(layer, width=2, color=(255, 255, 255, 255), style='solid'):
    """Apply border to layer."""
    if layer.mode != "RGBA":
        layer = layer.convert("RGBA")
    
    # Create border layer
    border_size = (
        layer.size[0] + width * 2,
        layer.size[1] + width * 2
    )
    border_layer = Image.new("RGBA", border_size, (0, 0, 0, 0))
    
    if style == 'solid':
        # Simple solid border
        draw = ImageDraw.Draw(border_layer)
        draw.rectangle([0, 0, border_size[0] - 1, border_size[1] - 1], 
                      outline=color, width=width)
    
    # Paste original layer
    border_layer.paste(layer, (width, width), layer)
    return border_layer


def scale_layer_with_quality(layer, new_size, method=Image.LANCZOS):
    """Scale layer with high quality resampling."""
    return layer.resize(new_size, method)


def crop_layer_to_content(layer, padding=0):
    """Crop layer to its non-transparent content with optional padding."""
    if layer.mode != "RGBA":
        return layer
    
    # Get bounding box of non-transparent pixels
    bbox = layer.getbbox()
    if bbox is None:
        return layer
    
    # Add padding
    left = max(0, bbox[0] - padding)
    top = max(0, bbox[1] - padding)
    right = min(layer.size[0], bbox[2] + padding)
    bottom = min(layer.size[1], bbox[3] + padding)
    
    return layer.crop((left, top, right, bottom))


def tile_layer(layer, target_size, mode='repeat'):
    """Tile layer to fill target size."""
    target_width, target_height = target_size
    layer_width, layer_height = layer.size
    
    if mode == 'repeat':
        result = Image.new(layer.mode, target_size)
        for y in range(0, target_height, layer_height):
            for x in range(0, target_width, layer_width):
                result.paste(layer, (x, y))
        return result
    elif mode == 'stretch':
        return layer.resize(target_size, Image.LANCZOS)
    else:
        return layer


def create_noise_layer(size, intensity=50, color=(255, 255, 255)):
    """Create noise layer."""
    width, height = size if isinstance(size, tuple) else (size, size)
    
    # Generate noise
    noise = np.random.randint(-intensity, intensity + 1, (height, width, 3))
    base = np.full((height, width, 3), color[:3], dtype=np.int16)
    
    # Add noise to base color
    result = np.clip(base + noise, 0, 255).astype(np.uint8)
    
    # Add alpha channel
    alpha = np.full((height, width, 1), 255, dtype=np.uint8)
    result_rgba = np.concatenate([result, alpha], axis=2)
    
    return Image.fromarray(result_rgba, "RGBA")


def flatten_layers(layers):
    """Flatten multiple layers into single image."""
    if not layers:
        return None
    
    result = layers[0].copy()
    for layer in layers[1:]:
        if layer.size != result.size:
            layer = layer.resize(result.size, Image.LANCZOS)
        result = Image.alpha_composite(result, layer)
    
    return result


def rotate_layer_with_padding(layer, angle, expand=True):
    """Rotate layer with automatic padding to prevent clipping."""
    if expand:
        return layer.rotate(angle, expand=True, fillcolor=(0, 0, 0, 0))
    else:
        return layer.rotate(angle, fillcolor=(0, 0, 0, 0))