# shapes/__init__.py
# Auto-discovery and import of shape modules

import os
import importlib

# Get current directory
current_dir = os.path.dirname(__file__)

# Auto-discover shape files
shape_files = [f[:-3] for f in os.listdir(current_dir) 
               if f.endswith('.py') and f != '__init__.py' and not f.startswith('_')]

# Build SHAPE_MAP by importing modules
SHAPE_MAP = {}
for shape_name in shape_files:
    try:
        module = importlib.import_module(f'.{shape_name}', package='banner.shapes')
        if hasattr(module, f'apply_{shape_name}'):
            SHAPE_MAP[shape_name] = getattr(module, f'apply_{shape_name}')
    except ImportError:
        pass

# Export the map
__all__ = ['SHAPE_MAP']