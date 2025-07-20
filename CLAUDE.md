# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Session Continuity

When starting a new conversation:
1. Always check git status to see modified files
2. Ask user "son kaldığımız yeri hatırlıyor musun?" to understand current work context
3. Read .claude/session_memory.md to understand where we left off
4. If user mentions system crashes/interruptions, implement recovery measures:
   - Check modified files for work in progress
   - Create checkpoint commits before major changes
   - Use TodoWrite to track progress and prevent loss
   - Update session memory with current progress
   - Save important decisions and context in commit messages

Session memory is maintained in .claude/session_memory.md - always update this file with:
- Current task/focus
- Modified files
- Key decisions made
- Next steps planned
- Any blockers or issues encountered

## Project Overview

GitHub Banner Maker is a Python tool for generating customizable banners for GitHub projects. It creates professional-looking 1024x256px banners with titles, subtitles, icons, gradients, textures, and effects using the Pillow (PIL) library.

## Commands

### Installation and Setup
```bash
pip install -r requirements.txt
```

### Basic Usage
```bash
# Generate simple banner with preset
python banner_maker.py --preset modern_blue --title "My Project"

# Custom banner with compact syntax
python banner_maker.py --title "My Project" --bg "blue:purple:diagonal" --pattern "dots:white:30"

# With icon
python banner_maker.py --title "My Project" --icon logo.png --accent "blue"

# Generate demo set with variations
python banner_maker.py --demo-set

# Learn CLI equivalent of preset
python banner_maker.py --learn ocean_waves
```

### New CLI System Features
```bash
# Compact multi-value parameters
python banner_maker.py --title "API Docs" --bg "orange:red:diagonal" --pattern "dots:white:25" --shape "wave:blue:60"

# Smart modifiers
python banner_maker.py --preset modern_blue --title "My Project" --accent "red" --intensity "high" --rounded "20"

# Get full help
python banner_maker.py --help-full
```

### Demo Generation
```bash
# Generate full demo set (60 variations)
python banner_maker.py --demo-set

# Single demo banner
python demo/demo.py
```

### Testing
No formal test framework is configured. The project uses demo generation for validation.

## Architecture

### Core Components

1. **banner_maker.py** - Main CLI entry point with modern compact parameter system
2. **core/cli_parser_v2.py** - New CLI parser with compact multi-value syntax
3. **core/compact_parser.py** - Compact parameter parsing ("blue:purple:diagonal" format)
4. **core/parameter_definitions.py** - Parameter definitions and help system
5. **banner/pipeline.py** - Core rendering pipeline with BannerConfig dataclass and layer-based rendering
6. **core/preset.py** - Preset system that loads JSON configurations from core/presets/
7. **banner/** modules - Specialized rendering components:
   - background.py - Gradient backgrounds and rounded rectangles
   - text.py - Text rendering with auto-sizing and contrast
   - icon.py - Icon processing and positioning
   - effects.py - Shadow, border, and visual effects
   - textures.py - Background textures (noise, dots, lines, etc.)
   - motifs.py - Decorative patterns and motifs
   - overlays.py - Overlay effects
   - shapes.py - Shape rendering

### Rendering Pipeline

The banner generation follows a layered approach in banner/pipeline.py:
1. Background layer (gradients)
2. Shape layer
3. Motif layer (decorative patterns)
4. Icon layer
5. Text layer
6. Texture layer
7. Effects layer
8. Overlay layer
9. Mask layer (rounded corners/borders)
10. Border layer

### Configuration System

- **BannerConfig dataclass** (pipeline.py:19-90) - Central configuration with 60+ parameters
- **JSON presets** (core/presets/*.json) - 30+ built-in design presets
- **CLI arguments** (banner_maker.py:13-43) - Auto-generated from BannerConfig fields
- **parameters.json** - Parameter metadata for documentation

### Core Utilities (DRY Refactoring)

The codebase has been refactored to follow DRY principles with centralized utilities:

- **core/color_utils.py** - All color operations, parsing, and contrast calculations
- **core/geometry_utils.py** - Gradients, shapes, masks, and geometric calculations
- **core/layer_utils.py** - Image composition, layer effects, and blending
- **core/config_utils.py** - Parameter extraction, validation, and configuration helpers
- **core/font_utils.py** - Font loading, text measurement, and typography utilities
- **core/constants.py** - All magic numbers, default values, and configuration constants

### Key Features

- **Auto-sizing text** - Automatically fits titles/subtitles to available space
- **Color extraction** - Dominant color detection from icons when auto_color=True
- **Supersampling** - 2x rendering with LANCZOS downsampling for quality
- **Modular textures** - Pluggable texture system via TEXTURE_MAP
- **Preset inheritance** - CLI args override preset values
- **Global ready** - English-only codebase for international use

## Development Principles

### DRY + KISS Philosophy

This project follows two core principles:

**DRY (Don't Repeat Yourself):**
- Eliminate code duplication through shared utilities
- Single source of truth for all common operations
- Centralized constants and configuration handling

**KISS (Keep It Simple, Stupid):**
- Simple functions over complex classes
- Clear, readable implementations
- Avoid over-engineering and premature optimization
- Prefer explicit code over "clever" abstractions

### Global Development Standards

**English-Only Codebase:**
- All variable names, comments, and documentation in English
- No localized strings or non-English identifiers
- International developer-friendly naming conventions

**Code Quality Guidelines:**
- Functions should do one thing well
- Prefer composition over complex inheritance
- Use clear, descriptive names
- Hardcode sensible defaults rather than over-configuring
- Delete unused code rather than commenting it out

### Refactoring Approach

When making changes:
1. **Check for duplication** - Use existing utilities before creating new ones
2. **Keep it simple** - Avoid adding unnecessary complexity
3. **English naming** - Ensure all new code uses English identifiers
4. **Single responsibility** - Each function should have one clear purpose
5. **Test existing functionality** - Ensure changes don't break banner generation

### File Structure Notes

- **fonts/** - DejaVu and Inter font files
- **demos/** - Generated example banners and demo grid
- **core/presets/** - 30 JSON preset files with design configurations
- **core/** - Centralized utility modules (post-DRY refactoring)
- Uses dataclasses extensively for configuration management

## Team Communication Guidelines

- **Collaboration Etiquette**
  - bana ne yapmayı düşündüğünü söylemeden ve onay almadan işe başlama lütfen

## Memory Log

- Her zaman nerede kaldığımızın izini tutmalıyız, bunu daha önce yapmıştık, her an bağlantımız kopabilecekmiş gibi davranmalıyız, güncellemelere başlamadan önce mutlaka hafızayı tazele