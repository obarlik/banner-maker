# textures/_utils.py
# Shared utilities for texture generation

import numpy as np
from PIL import Image

def calculate_normal_map_from_heightmap(heightmap, strength=1.0):
    """
    Calculate normal map from heightmap using gradient.
    Simple version without mesh triangulation.
    """
    h, w = heightmap.shape
    
    # Calculate gradients (sobel-like)
    # Pad the heightmap to handle edges
    padded = np.pad(heightmap, 1, mode='edge')
    
    # Calculate gradients
    dx = (padded[1:-1, 2:] - padded[1:-1, :-2]) / 2.0
    dy = (padded[2:, 1:-1] - padded[:-2, 1:-1]) / 2.0
    
    # Calculate normal vectors
    # Normal = (-dx, -dy, 1) normalized
    dz = np.ones_like(dx) / strength
    
    # Normalize
    length = np.sqrt(dx*dx + dy*dy + dz*dz)
    nx = -dx / length
    ny = -dy / length  
    nz = dz / length
    
    # Convert to [0, 255] range
    normal_map = np.zeros((h, w, 3), dtype=np.uint8)
    normal_map[:, :, 0] = ((nx + 1) * 127.5).astype(np.uint8)  # Red = X
    normal_map[:, :, 1] = ((ny + 1) * 127.5).astype(np.uint8)  # Green = Y  
    normal_map[:, :, 2] = ((nz + 1) * 127.5).astype(np.uint8)  # Blue = Z
    
    return normal_map

def apply_lighting_to_image(img_array, normal_map, light_dir=(-0.5, -0.5, 1.0), ambient=0.3):
    """
    Apply lighting to image using normal map.
    """
    # Normalize light direction
    light_dir = np.array(light_dir)
    light_dir = light_dir / np.linalg.norm(light_dir)
    
    # Convert normal map back to [-1, 1] range
    normal_map_processed = (normal_map.astype(np.float32) / 127.5) - 1
    
    # Calculate diffuse lighting (dot product)
    diffuse = np.sum(normal_map_processed * light_dir, axis=2)
    diffuse = np.clip(diffuse, 0, 1)  # Only positive lighting
    
    # Combine ambient + diffuse
    lighting = ambient + (1 - ambient) * diffuse
    
    # Apply lighting to image
    if img_array.shape[-1] == 4:  # RGBA
        lit_img = img_array.copy()
        lit_img[:, :, :3] = (lit_img[:, :, :3] * lighting[..., np.newaxis]).astype(np.uint8)
    else:  # RGB
        lit_img = (img_array * lighting[..., np.newaxis]).astype(np.uint8)
    
    return lit_img

def calculate_normal_map(heightmap, vertices, tri_simplices, strength=2.5):
    """
    Function that calculates a single normal vector for each triangle
    """
    H, W = heightmap.shape
    normal_map = np.zeros((H, W, 3), dtype=np.float32)
    
    # Calculate normal for each triangle
    for simplex in tri_simplices:
        # Get triangle corner points
        v0, v1, v2 = vertices[simplex]
        x0, y0 = v0
        x1, y1 = v1
        x2, y2 = v2
        
        # Height values of corners
        z0 = heightmap[int(y0), int(x0)]
        z1 = heightmap[int(y1), int(x1)]
        z2 = heightmap[int(y2), int(x2)]
        
        # Two vectors of the triangle
        vec1 = np.array([x1-x0, y1-y0, z1-z0])
        vec2 = np.array([x2-x0, y2-y0, z2-z0])
        
        # Normal vector (cross product)
        normal = np.cross(vec1, vec2)
        normal = normal / (np.linalg.norm(normal) + 1e-8)  # normalize
        
        # Find triangle boundaries
        min_x, max_x = int(min(x0, x1, x2)), int(max(x0, x1, x2)) + 1
        min_y, max_y = int(min(y0, y1, y2)), int(max(y0, y1, y2)) + 1
        
        # Assign this normal to all pixels within the triangle
        for x in range(max(0, min_x), min(W, max_x)):
            for y in range(max(0, min_y), min(H, max_y)):
                # Calculate barycentric coordinates
                denom = (y1 - y2)*(x0 - x2) + (x2 - x1)*(y0 - y2)
                if abs(denom) < 1e-8:
                    continue
                a = ((y1 - y2)*(x - x2) + (x2 - x1)*(y - y2)) / denom
                b = ((y2 - y0)*(x - x2) + (x0 - x2)*(y - y2)) / denom
                c = 1 - a - b
                
                # If pixel is inside triangle
                if 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1:
                    normal_map[y, x] = normal
    
    # Edge highlighting
    if strength > 0:
        dzdx = np.gradient(heightmap, axis=1) * strength * 3.0
        dzdy = np.gradient(heightmap, axis=0) * strength * 3.0
        
        edge_strength = np.sqrt(dzdx**2 + dzdy**2)
        edge_mask = (edge_strength > np.percentile(edge_strength, 70)).astype(float)
        
        normal_map[..., 0] -= edge_mask * dzdx * 0.7
        normal_map[..., 1] -= edge_mask * dzdy * 0.7
    
    # Bring normal map to [0,1] range
    normal_map = (normal_map + 1) / 2  # [-1,1] -> [0,1]
    return (normal_map * 255).clip(0, 255).astype(np.uint8)