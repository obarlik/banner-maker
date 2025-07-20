import numpy as np
from PIL import Image

# --- Mesh-based normal calculation ---
def compute_vertex_normals(vertices, triangles):
    normals = np.zeros_like(vertices)
    for tri in triangles:
        v0, v1, v2 = vertices[tri]
        n = np.cross(v1-v0, v2-v0)
        n = n / (np.linalg.norm(n)+1e-8)
        for vi in tri:
            normals[vi] += n
    normals = normals / (np.linalg.norm(normals, axis=1, keepdims=True)+1e-8)
    return normals

# --- Triangle rasterization with barycentric coordinates + texture mapping ---
def triangle_rasterize(img, v, z, n, uv, img_texture, light_dir=(1,0,1), shading='lambert', zbuf=None):
    # v: (3,2), z: (3,), n: (3,3), uv: (3,2)
    H, W = img.shape[:2]
    tex_h, tex_w = img_texture.shape[:2]
    x0, y0 = v[0]
    x1, y1 = v[1]
    x2, y2 = v[2]
    minx = max(int(np.floor(min(x0, x1, x2))), 0)
    maxx = min(int(np.ceil(max(x0, x1, x2))), W-1)
    miny = max(int(np.floor(min(y0, y1, y2))), 0)
    maxy = min(int(np.ceil(max(y0, y1, y2))), H-1)
    denom = (y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
    if abs(denom) < 1e-8:
        return
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            w0 = ((y1-y2)*(x-x2)+(x2-x1)*(y-y2))/denom
            w1 = ((y2-y0)*(x-x2)+(x0-x2)*(y-y2))/denom
            w2 = 1 - w0 - w1
            if w0 < 0 or w1 < 0 or w2 < 0:
                continue
            zz = w0*z[0] + w1*z[1] + w2*z[2]
            if zbuf is not None and zz < zbuf[y, x]:
                continue
            nn = w0*n[0] + w1*n[1] + w2*n[2]
            nn = nn / (np.linalg.norm(nn)+1e-8)
            uv_interp = w0*uv[0] + w1*uv[1] + w2*uv[2]
            tx = int(np.clip(uv_interp[0]*tex_w, 0, tex_w-1))
            ty = int(np.clip(uv_interp[1]*tex_h, 0, tex_h-1))
            tex_color = img_texture[ty, tx, :3]
            if shading == 'lambert':
                diff = max(np.dot(nn, light_dir)/np.linalg.norm(light_dir), 0.0)
                diff = pow(diff, 0.5)  # More contrasty shadow
                c = tex_color * (0.5 + 0.5*diff)
            else:
                c = tex_color
            img[y, x] = np.clip(c, 0, 255)
            if zbuf is not None:
                zbuf[y, x] = zz

# --- Mesh rasterization (texture mapping + shading) ---
def rasterize_mesh(vertices, triangles, normals, z, uvs, img_texture, light_dir=(1,0,1), shading='lambert', out_shape=None):
    if out_shape is None:
        H = int(vertices[:,1].max())+1
        W = int(vertices[:,0].max())+1
    else:
        H, W = out_shape
    img = np.zeros((H, W, 3), dtype=np.float32)
    zbuf = np.full((H, W), -np.inf, dtype=np.float32)
    for tri in triangles:
        v = vertices[tri, :2]
        zz = z[tri]
        n = normals[tri]
        uv = uvs[tri]
        triangle_rasterize(img, v, zz, n, uv, img_texture, light_dir, shading, zbuf)
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), mode='RGB')

# --- Lambertian shading helper function ---
def lambertian_shading(normals, light_dir=(1,0,1), base_color=(200,200,200)):
    light_dir = np.array(light_dir, dtype=np.float32)
    light_dir = light_dir / (np.linalg.norm(light_dir)+1e-8)
    diff = np.dot(normals, light_dir)
    diff = np.clip(diff, 0, 1)
    color = np.array(base_color, dtype=np.float32)[None, :]
    shaded = color * (0.08 + 0.92*diff[:,None])
    return shaded.astype(np.uint8)

# --- Extensible: normal map, debug visuals, etc. --- 