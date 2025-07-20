# image_utils.py
from PIL import Image, ImageDraw
import numpy as np

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    return tuple(int(hex_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def get_dominant_colors(image_path, n=2):
    try:
        img = Image.open(image_path).convert('RGB').resize((64, 64))
        colors = img.getcolors(64*64)
        colors.sort(reverse=True)
        dominant = [c[1] for c in colors[:n]]
        while len(dominant) < n:
            dominant.append((0, 82, 204))
        return dominant
    except Exception:
        return [(0, 82, 204)] * n

def get_average_color(colors):
    r = int(sum([c[0] for c in colors]) / len(colors))
    g = int(sum([c[1] for c in colors]) / len(colors))
    b = int(sum([c[2] for c in colors]) / len(colors))
    return (r, g, b)

def get_contrast_color(rgb):
    yiq = ((rgb[0]*299)+(rgb[1]*587)+(rgb[2]*114))/1000
    return (0,0,0) if yiq >= 128 else (255,255,255)

def get_outline_color(rgb):
    return (0,0,0) if contrast_ratio(rgb, (0,0,0)) > contrast_ratio(rgb, (255,255,255)) else (255,255,255)

def gradient_vertical(img, box, start, end):
    draw = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    w, h = x1-x0+1, y1-y0+1
    for y in range(y0, y1+1):
        ratio = (y-y0) / max(1, h-1)
        r = int(start[0] * (1 - ratio) + end[0] * ratio)
        g = int(start[1] * (1 - ratio) + end[1] * ratio)
        b = int(start[2] * (1 - ratio) + end[2] * ratio)
        draw.line([(x0, y), (x1, y)], fill=(r, g, b, 255))

def gradient_horizontal(img, box, start, end):
    draw = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    w, h = x1-x0+1, y1-y0+1
    for x in range(x0, x1+1):
        ratio = (x-x0) / max(1, w-1)
        r = int(start[0] * (1 - ratio) + end[0] * ratio)
        g = int(start[1] * (1 - ratio) + end[1] * ratio)
        b = int(start[2] * (1 - ratio) + end[2] * ratio)
        draw.line([(x, y0), (x, y1)], fill=(r, g, b, 255))

def gradient_diagonal(img, box, start, end):
    draw = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    w, h = x1-x0+1, y1-y0+1
    for i in range(max(w, h)):
        ratio = i / max(1, max(w, h)-1)
        r = int(start[0] * (1 - ratio) + end[0] * ratio)
        g = int(start[1] * (1 - ratio) + end[1] * ratio)
        b = int(start[2] * (1 - ratio) + end[2] * ratio)
        x = int(x0 + i * w / max(w, h))
        y = int(y0 + i * h / max(w, h))
        draw.line([(x0, y), (x, y1)], fill=(r, g, b, 255))

def gradient_radial(img, box, start, end):
    x0, y0, x1, y1 = box
    w, h = x1-x0+1, y1-y0+1
    cx, cy = (x0+x1)//2, (y0+y1)//2
    maxr = ((w/2)**2 + (h/2)**2) ** 0.5
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            dist = ((x-cx)**2 + (y-cy)**2) ** 0.5
            ratio = min(1, dist / maxr)
            r = int(start[0] * (1 - ratio) + end[0] * ratio)
            g = int(start[1] * (1 - ratio) + end[1] * ratio)
            b = int(start[2] * (1 - ratio) + end[2] * ratio)
            img.putpixel((x, y), (r, g, b, 255))

GRADIENT_MAP = {
    "vertical": gradient_vertical,
    "horizontal": gradient_horizontal,
    "diagonal": gradient_diagonal,
    "radial": gradient_radial,
}

def draw_gradient_custom(img, box, start, end, grad_type="vertical"):
    func = GRADIENT_MAP.get(grad_type, gradient_vertical)
    func(img, box, start, end)

def draw_asym_rounded_rectangle(draw, box, radii, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = box
    tl, tr, br, bl = radii
    draw.pieslice([x0, y0, x0+2*tl, y0+2*tl], 180, 270, fill=fill)
    draw.pieslice([x1-2*tr, y0, x1, y0+2*tr], 270, 360, fill=fill)
    draw.pieslice([x1-2*br, y1-2*br, x1, y1], 0, 90, fill=fill)
    draw.pieslice([x0, y1-2*bl, x0+2*bl, y1], 90, 180, fill=fill)
    draw.rectangle([x0+tl, y0, x1-tr, y0+max(tl,tr)], fill=fill)
    draw.rectangle([x0, y0+tl, x0+max(tl,bl), y1-bl], fill=fill)
    draw.rectangle([x1-max(tr,br), y0+tr, x1, y1-br], fill=fill)
    draw.rectangle([x0+bl, y1-max(bl,br), x1-br, y1], fill=fill)
    draw.rectangle([x0+tl, y0+max(tl,tr), x1-tr, y1-max(bl,br)], fill=fill)
    if outline:
        pass

def draw_gradient(draw, width, height, start, end):
    for y in range(height):
        ratio = y / height
        r = int(start[0] * (1 - ratio) + end[0] * ratio)
        g = int(start[1] * (1 - ratio) + end[1] * ratio)
        b = int(start[2] * (1 - ratio) + end[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def rgb_distance(c1, c2):
    return ((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2) ** 0.5

def adjust_color(c, delta):
    return tuple(max(0, min(255, x+delta)) for x in c)

def luminance(rgb):
    def channel(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 * 255 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

def contrast_ratio(rgb1, rgb2):
    l1 = luminance(rgb1)
    l2 = luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05) 