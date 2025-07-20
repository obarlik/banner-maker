import os
import json

PRESET_DIR = os.path.join(os.path.dirname(__file__), 'presets')

# Load all preset json files at startup
PRESET_LIST = []
for fname in os.listdir(PRESET_DIR):
    if fname.endswith('.json'):
        name = fname[:-5]
        with open(os.path.join(PRESET_DIR, fname), encoding='utf-8') as f:
            data = json.load(f)
        PRESET_LIST.append((name, data))

presets = [p[1] for p in PRESET_LIST]
preset_names = [p[0] for p in PRESET_LIST] 

def load_preset(preset_name):
    """Load preset configuration by name."""
    if preset_name in preset_names:
        idx = preset_names.index(preset_name)
        return presets[idx].copy()
    return None

def get_available_presets():
    """Get list of available preset names."""
    return preset_names.copy()

class BannerConfig:
    texture_scale: float = 0.3
    texture_displacement_strength: float = 3.0
    texture_shading_strength: float = 1.0 