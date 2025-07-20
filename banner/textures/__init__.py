# textures/__init__.py
# Auto-discovery and import of texture modules

import os
import importlib

# Get current directory
current_dir = os.path.dirname(__file__)

# Auto-discover texture files
texture_files = [f[:-3] for f in os.listdir(current_dir) 
                 if f.endswith('.py') and f != '__init__.py' and not f.startswith('_')]

# Build TEXTURE_MAP by importing modules
TEXTURE_MAP = {}
for texture_name in texture_files:
    try:
        module = importlib.import_module(f'.{texture_name}', package='banner.textures')
        if hasattr(module, f'apply_{texture_name}'):
            TEXTURE_MAP[texture_name] = getattr(module, f'apply_{texture_name}')
    except ImportError:
        pass

# Export the map
__all__ = ['TEXTURE_MAP']