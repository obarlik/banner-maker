from banner.pipeline import generate_banner, BannerConfig
from core.preset import presets, preset_names
import os
import json
import sys

from demo.demo import create_demo_grid


def generate_demo_set(args_dict):
    """Generate demo banner set using all available presets."""
    print("\n--- Demo Banner Set Generator ---")
    user_title = args_dict.get('title', 'Banner Maker')
    user_subtitle = args_dict.get('subtitle', 'Customizable Project Banner Generator')
    user_icon = args_dict.get('icon', None)
    
    demo_dir = os.path.join(os.path.dirname(args_dict.get('output', 'github_banner.png')), "demos")
    os.makedirs(demo_dir, exist_ok=True)
    demo_log_path = os.path.join(demo_dir, "demo_log.txt")
    
    # Generate demo for each preset
    demo_count = len(presets)
    log_lines = []
    
    for idx in range(1, demo_count + 1):
        demo = presets[idx - 1].copy()
        demo["preset_name"] = preset_names[idx - 1]
        
        # Generate banner
        out_name = f"demo_{idx:02d}.png"
        out_path = os.path.join(demo_dir, out_name)
        print(f"Generating demo: {out_name} ({demo['preset_name']})")
        
        demo_config = demo.copy()
        demo_config["title"] = user_title
        demo_config["subtitle"] = user_subtitle
        demo_config["icon_path"] = user_icon
        demo_config["output"] = out_path
        
        # Filter to only include valid BannerConfig fields
        banner_fields = set(BannerConfig.__dataclass_fields__.keys())
        filtered_config = {k: v for k, v in demo_config.items() if k in banner_fields}
        config = BannerConfig(**filtered_config)
        generate_banner(config)
        
        # Log entry
        log_lines.append(f"{out_name}: preset={demo['preset_name']}, params={json.dumps(demo, ensure_ascii=False)}")
    
    # Write log file
    with open(demo_log_path, "w", encoding="utf-8") as f:
        f.write(f"Banner Title: {user_title}\nBanner Subtitle: {user_subtitle}\nBanner Icon: {user_icon}\n\n")
        for line in log_lines:
            f.write(line + "\n")
    
    print(f"\nDemo banners saved to {demo_dir} folder.\nFor parameters: {demo_log_path}\n")
    
    # Create demo grid
    create_demo_grid(
        demo_dir, 
        gutter=12, 
        label_h=48, 
        label_font_size=14, 
        label_padding=6, 
        label_radius=8, 
        label_line_spacing=2, 
        grid_bg=(30, 30, 30, 255)
    )
    
    sys.exit(0)