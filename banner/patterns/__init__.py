# Auto-import all pattern variations and build PATTERN_MAP
import os
import importlib

# Common imports and utilities for all patterns
import random
from PIL import Image, ImageDraw
import numpy as np
from core.color_utils import parse_color, get_random_rotation

# Auto-discover and import all pattern modules
PATTERN_MAP = {}
current_dir = os.path.dirname(__file__)

# Get all .py files in patterns directory (excluding __init__.py)
pattern_files = [f[:-3] for f in os.listdir(current_dir) 
                if f.endswith('.py') and f != '__init__.py']

# Import each pattern module and add to PATTERN_MAP
for pattern_name in pattern_files:
    try:
        module = importlib.import_module(f'banner.patterns.{pattern_name}')
        # Look for apply_* functions in the module
        for attr_name in dir(module):
            if attr_name.startswith('apply_'):
                func = getattr(module, attr_name)
                # Use the function name without 'apply_' prefix
                map_name = attr_name[6:]  # Remove 'apply_' prefix
                PATTERN_MAP[map_name] = func
    except ImportError as e:
        print(f"Warning: Could not import pattern {pattern_name}: {e}")

# Export the map
__all__ = ['PATTERN_MAP']