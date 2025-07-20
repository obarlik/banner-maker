from banner.pipeline import generate_banner, BannerConfig
from banner.textures import TEXTURE_MAP
from core.preset import presets, preset_names
import os
import random
import json
import sys
from dataclasses import fields

from demo.demo import create_demo_grid, param_summary
from banner.overlays import OVERLAY_MAP
from banner.shapes import SHAPE_MAP
from banner.patterns import PATTERN_MAP

DEMO_DEFAULTS_JSON = os.path.join(os.path.dirname(__file__), '..', 'demo_defaults.json')

def load_demo_defaults():
    with open(DEMO_DEFAULTS_JSON, encoding='utf-8') as f:
        return json.load(f)

# --- Random parameter generator functions ---
def random_overlay_params(overlay):
    import random
    if overlay == "color":
        return {
            "overlay_color": [random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(40,120)],
            "overlay_blur": random.choice([0, 8, 16])
        }
    elif overlay == "gradient":
        return {
            "overlay_color1": [random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,120)],
            "overlay_color2": [random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,120)],
            "overlay_direction": random.choice(["vertical", "horizontal", "diagonal"]),
            "overlay_blur": random.choice([0, 8, 16])
        }
    elif overlay == "lens_flare":
        return {
            "overlay_center": [random.randint(200,900), random.randint(40,180)],
            "overlay_radius": random.randint(60,180),
            "overlay_color": [255,255,220,random.randint(120,220)],
            "overlay_intensity": round(random.uniform(0.7,1.2),2),
            "overlay_rings": random.randint(2,5),
            "overlay_blur": random.choice([24,32,40])
        }
    return {}

def random_shape_params(shape):
    import random
    if shape == "wave":
        return {
            "shape_color": [random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(40,120)],
            "shape_amplitude": round(random.uniform(0.12,0.22),2),
            "shape_frequency": random.randint(1,3),
            "shape_blur": random.choice([8,16,24])
        }
    elif shape == "blob":
        return {
            "shape_color": [random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(40,120)],
            "shape_seed": random.randint(1,100),
            "shape_scale": round(random.uniform(0.5,0.9),2),
            "shape_blur": random.choice([16,24,32])
        }
    elif shape == "polygon":
        return {
            "shape_color": [random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(40,120)],
            "shape_sides": random.randint(3,8),
            "shape_radius": random.randint(60,140),
            "shape_rotation": random.choice([0,15,30,45,60]),
            "shape_blur": random.choice([8,16,24])
        }
    elif shape == "ellipse":
        return {
            "shape_color": [random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(40,120)],
            "shape_center": [random.randint(200,900), random.randint(40,180)],
            "shape_rx": random.randint(80,220),
            "shape_ry": random.randint(40,120),
            "shape_blur": random.choice([8,16,24])
        }
    elif shape == "diagonal_bar":
        return {
            "shape_color": [random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(40,120)],
            "shape_angle": random.choice([15,30,45,60]),
            "shape_thickness": round(random.uniform(0.15,0.35),2),
            "shape_blur": random.choice([8,16,24])
        }
    return {}

def random_motif_params(motif):
    import random
    if motif == "none":
        return {"motif_opacity": 0}
    
    # Base parameters
    base_density = round(random.uniform(0.7, 1.5), 2)
    base_opacity = random.randint(30, 120)
    
    # Pattern-specific controls based on visual impact
    if motif in ['squares', 'rectangles']:
        # Square patterns are very dominant - heavily reduce density
        base_density = round(random.uniform(0.3, 0.6), 2)
        base_opacity = random.randint(20, 50)
    elif motif in ['triangles', 'triangles_outline']:
        # Triangles are angular and attention-grabbing
        base_density = round(random.uniform(0.5, 0.8), 2)
        base_opacity = random.randint(30, 70)
    elif motif in ['stars', 'stars_outline', 'hearts', 'hearts_outline']:
        # Complex patterns: moderate density
        base_density = round(random.uniform(0.6, 1.0), 2)
        base_opacity = random.randint(40, 80)
    elif motif in ['dots', 'circles']:
        # Small patterns: can handle higher density
        base_density = round(random.uniform(0.8, 1.3), 2)
        base_opacity = random.randint(50, 100)
    elif motif in ['lines', 'sine', 'zigzag']:
        # Line patterns: moderate density
        base_density = round(random.uniform(0.7, 1.1), 2)
        base_opacity = random.randint(40, 90)
    
    return {
        "motif_density": base_density,
        "motif_opacity": base_opacity,
        "motif_colors": [[random.randint(0,255), random.randint(0,255), random.randint(0,255)] for _ in range(random.randint(1,3))],
        "motif_rotation": random.choice([0, 15, 30, 45, 60, 90]),
        "motif_jitter": round(random.uniform(0, 0.3), 2),
        "motif_size_variance": round(random.uniform(0, 0.3), 2)
    }

def random_texture_params(texture):
    import random
    if texture == "none":
        return {"texture_opacity": 0}
    return {
        "texture_density": round(random.uniform(0.5, 1.2), 2),
        "texture_opacity": random.randint(8, 24),
        "texture_rotation": random.choice([0, 45, 90, 180, 270, 360]),
        "texture_colors": [[random.randint(0,255), random.randint(0,255), random.randint(0,255)] for _ in range(random.randint(1,3))]
    }

def generate_demo_set(args_dict):
    demo_defaults = load_demo_defaults()
    print("\n--- Demo Banner Set Generator ---")
    user_title = args_dict.get('title', 'Banner Maker')
    user_subtitle = args_dict.get('subtitle', 'Customizable Project Banner Generator')
    user_icon = args_dict.get('icon', None)
    demo_dir = os.path.join(os.path.dirname(args_dict.get('output', 'github_banner.png')), "demos")
    os.makedirs(demo_dir, exist_ok=True)
    demo_log_path = os.path.join(demo_dir, "demo_log.txt")
    # All constants from json
    gradient_types = demo_defaults["gradient_types"]
    textures = list(TEXTURE_MAP.keys())
    label_font_sizes = demo_defaults["label_font_sizes"]
    label_hs = demo_defaults["label_hs"]
    label_paddings = demo_defaults["label_paddings"]
    label_radiuses = demo_defaults["label_radiuses"]
    label_line_spacings = demo_defaults["label_line_spacings"]
    grid_bgs = demo_defaults["grid_bgs"]
    bg_color_pairs = demo_defaults["bg_color_pairs"]
    text_colors = demo_defaults["text_colors"]
    icon_positions = demo_defaults["icon_positions"]
    rounded_opts = demo_defaults["rounded_opts"]
    shadow_opts = demo_defaults["shadow_opts"]
    border_opts = demo_defaults["border_opts"]
    title_font_sizes = demo_defaults["title_font_sizes"]
    subtitle_font_sizes = demo_defaults["subtitle_font_sizes"]
    min_contrast_range = demo_defaults["min_contrast_range"]
    texture_density_range = demo_defaults["texture_density_range"]
    texture_opacity_range = demo_defaults["texture_opacity_range"]
    cr_choices = demo_defaults["cr_choices"]
    overlays = demo_defaults["overlays"]
    # Only generate demos for existing presets
    demo_count = len(presets)
    log_lines = []
    
    for idx in range(1, demo_count+1):
        demo = presets[idx-1].copy()
        demo["preset_name"] = preset_names[idx-1]
        demo.setdefault("title_font_size", 64)
        demo.setdefault("subtitle_font_size", 28)
        demo.setdefault("icon_shadow", False)
        demo.setdefault("icon_outline", False)
        demo.setdefault("texture_density", 1.0)
        demo.setdefault("texture_opacity", 20)
        demo.setdefault("shadow_opacity", 100)
        demo.setdefault("label_font_size", 14)
        demo.setdefault("label_h", 32)
        demo.setdefault("label_padding", 6)
        demo.setdefault("label_radius", 8)
        demo.setdefault("label_line_spacing", 2)
        demo.setdefault("grid_bg", (30,30,30,255))
        demo.setdefault("overlay", "none")
        # Transfer motif parameters from preset if available, otherwise set defaults
        demo.setdefault('motif', 'none')
        demo.setdefault('motif_density', 1.0)
        demo.setdefault('motif_opacity', 0 if demo.get('motif', 'none')=='none' else 80)
        demo.setdefault('motif_colors', None)
        demo.setdefault('motif_rotation', 0)
        demo.setdefault('motif_jitter', 0.0)
        demo.setdefault('motif_size_variance', 0.0)
        # Preset values should not be overridden - they are the designed values
        out_name = f"demo_{idx:02d}.png"
        out_path = os.path.join(demo_dir, out_name)
        print(f"Generating demo: {out_name}")
        demo_config = demo.copy()
        demo_config["title"] = user_title
        demo_config["subtitle"] = user_subtitle
        demo_config["icon_path"] = user_icon
        demo_config["output"] = out_path
        # Include output parameter and all BannerConfig fields
        from banner.pipeline import BannerConfig
        banner_fields = set(BannerConfig.__dataclass_fields__.keys())
        filtered_config = {k: v for k, v in demo_config.items() if k in banner_fields}
        config = BannerConfig(**filtered_config)
        generate_banner(config)
        # --- LOG line updated ---
        if demo.get("preset_name"):
            log_lines.append(f"{out_name}: preset={demo['preset_name']}, params={json.dumps(demo, ensure_ascii=False)}")
        else:
            log_lines.append(f"{out_name}: params={json.dumps(demo, ensure_ascii=False)}")
    with open(demo_log_path, "w", encoding="utf-8") as f:
        f.write(f"Banner Title: {user_title}\nBanner Subtitle: {user_subtitle}\nBanner Icon: {user_icon}\n\n")
        for line in log_lines:
            f.write(line + "\n")
    print(f"\nDemo banners saved to {demo_dir} folder.\nFor parameters: {demo_log_path}\n")
    # Create demo grid (all parameters random)
    create_demo_grid(demo_dir, gutter=random.choice([8,10,12,14,16]), label_h=48, label_font_size=14, label_padding=6, label_radius=8, label_line_spacing=2, grid_bg=(30,30,30,255))
    sys.exit(0) 