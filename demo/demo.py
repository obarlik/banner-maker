def param_summary(d):
    grad = d.get('gradient_type', '-')
    tex = d.get('texture', '-')
    motif = d.get('motif', '-')
    motif_col = d.get('motif_colors', '-')
    motif_op = d.get('motif_opacity', '-')
    motif_den = d.get('motif_density', '-')
    cr = '/'.join(str(d.get(k,0) or 0) for k in ['corner_radius_tl','corner_radius_tr','corner_radius_br','corner_radius_bl'])
    contrast = f"{d.get('min_contrast',0):.1f}"
    shadow = str(d.get('shadow_opacity',0))
    opacity = str(d.get('texture_opacity',0))
    return f"grad:{grad}, tex:{tex}, motif:{motif}, mcol:{motif_col}, mop:{motif_op}, mden:{motif_den}, corner:{cr}, contrast:{contrast}, shadow:{shadow}, opacity:{opacity}"

def wrap_text(text, font, max_width, max_lines=3):
    from PIL import ImageDraw, Image
    draw = ImageDraw.Draw(Image.new("RGB", (1,1)))
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = current + (" " if current else "") + word
        bbox = draw.textbbox((0,0), test, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
        if len(lines) == max_lines:
            break
    if current and len(lines) < max_lines:
        lines.append(current)
    # If there are extra lines, truncate the last line
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    if len(lines) == max_lines and (len(words) > 0 and ' '.join(words) != ' '.join(lines)):
        # Truncate the last line
        while True:
            bbox = draw.textbbox((0,0), lines[-1] + '...', font=font)
            w = bbox[2] - bbox[0]
            if w <= max_width or len(lines[-1]) == 0:
                break
            lines[-1] = lines[-1][:-1]
        lines[-1] += '...'
    return '\n'.join(lines)

def create_demo_grid(demo_dir, tile_w=320, tile_h=80, cols=6, out_file="demo_grid.png", gutter=12, label_h=80, label_font_size=10, label_padding=6, label_radius=0, label_line_spacing=0, grid_bg=(30,30,30,255)):
    from PIL import Image, ImageDraw, ImageFont
    import glob, os, ast
    files = sorted(glob.glob(os.path.join(demo_dir, "demo_[0-9][0-9].png")))
    if not files:
        print("No demo images found for grid.")
        return
    rows = (len(files) + cols - 1) // cols
    grid_img = Image.new("RGBA", (tile_w*cols + gutter*(cols-1), (tile_h+label_h)*rows + gutter*(rows-1)), grid_bg)
    try:
        font = ImageFont.truetype("DejaVuSansMono-Bold.ttf", label_font_size)
    except:
        try:
            font = ImageFont.truetype("courbd.ttf", label_font_size)
        except:
            font = ImageFont.load_default()
    for idx, f in enumerate(files):
        row = idx // cols
        col = idx % cols
        im = Image.open(f).convert("RGBA").resize((tile_w, tile_h), Image.LANCZOS)
        if row == rows-1 and len(files)%cols != 0:
            offset = ((cols - (len(files)%cols)) * (tile_w + gutter)) // 2
            x = col * (tile_w + gutter) + offset
        else:
            x = col * (tile_w + gutter)
        y = row * ((tile_h + label_h) + gutter)
        grid_img.paste(im, (x, y))
        log_path = os.path.join(demo_dir, "demo_log.txt")
        label = os.path.splitext(os.path.basename(f))[0]
        param = ""
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as lf:
                for line in lf:
                    if line.startswith(label):
                        try:
                            d = ast.literal_eval(line.split(":",1)[-1].strip())
                            param = param_summary(d)
                        except Exception:
                            param = line.split(":",1)[-1].strip()
                        break
        if param:
            label_text = wrap_text(param, font, tile_w-2*label_padding, max_lines=3)
        else:
            label_text = label
        draw = ImageDraw.Draw(grid_img)
        label_box = [x, y+tile_h, x+tile_w, y+tile_h+label_h]
        label_radius = max(label_radius, 8)
        try:
            draw.rounded_rectangle(label_box, radius=label_radius, fill=(0,0,0,220))
        except:
            draw.rectangle(label_box, fill=(0,0,0,220))
        draw.text((x+label_padding, y+tile_h+label_padding), label_text, font=font, fill=(255,255,255,220), spacing=max(label_line_spacing,2))
    out_path = os.path.join(demo_dir, out_file)
    grid_img.save(out_path)
    print(f"Demo grid saved as {out_path}") 