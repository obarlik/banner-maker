# Preset Gallery

This document showcases all available design presets for Banner Maker. Each preset is a carefully crafted combination of colors, gradients, patterns, shapes, textures, and effects.

## Quick Usage

```bash
# Use any preset with your content
python banner_maker.py --preset PRESET_NAME --title "Your Title" --subtitle "Your Subtitle"

# Learn the CLI equivalent of any preset
python banner_maker.py --learn PRESET_NAME
```

## Featured Presets

### Modern Blue
**Perfect for:** Professional projects, corporate branding, tech startups
```bash
python banner_maker.py --preset modern_blue --title "Your Project"
```
![Modern Blue](presets/modern_blue.png)

### Geometric Chaos
**Perfect for:** Creative projects, design portfolios, artistic endeavors
```bash
python banner_maker.py --preset geometric_chaos --title "Your Project"
```
![Geometric Chaos](presets/geometric_chaos.png)

### Vaporwave
**Perfect for:** Retro projects, gaming, nostalgic themes
```bash
python banner_maker.py --preset vaporwave --title "Your Project"
```
![Vaporwave](presets/vaporwave.png)

### Ocean Waves
**Perfect for:** Nature projects, environmental themes, calming designs
```bash
python banner_maker.py --preset ocean_waves --title "Your Project"
```
![Ocean Waves](presets/ocean_waves.png)

### Vintage Leather
**Perfect for:** Classic projects, luxury branding, traditional themes
```bash
python banner_maker.py --preset vintage_leather --title "Your Project"
```
![Vintage Leather](presets/vintage_leather.png)

### Cyber Yellow
**Perfect for:** Tech projects, futuristic themes, innovative products
```bash
python banner_maker.py --preset cyber_yellow --title "Your Project"
```
![Cyber Yellow](presets/cyber_yellow.png)

## Complete Preset List

### Professional & Business
- **modern_blue** - Clean professional design with blue gradients
- **business_green** - Corporate green theme for business projects
- **github_pro** - GitHub-inspired professional styling
- **fintech_gold** - Premium gold theme for financial projects
- **dark_portfolio** - Sleek dark theme for portfolios

### Creative & Artistic
- **geometric_chaos** - Dynamic triangular patterns with vibrant colors
- **polygon_constellation** - Star-filled geometric wonderland
- **blob_garden** - Organic flowing shapes and natural colors
- **organic_blobs** - Soft, natural blob shapes with earth tones
- **layered_shapes** - Multiple overlapping geometric elements

### Tech & Futuristic
- **cyber_yellow** - Bold yellow tech aesthetic
- **purple_tech** - Purple gradients with technological feel
- **matrix_grid** - Digital matrix-inspired grid patterns
- **neon_retro** - Bright neon colors with retro vibes

### Nature & Organic
- **nature_breeze** - Fresh green natural themes
- **ocean_waves** - Flowing wave patterns with ocean colors
- **water_reflection** - Calming water-inspired designs
- **wave_dynamics** - Dynamic wave patterns and movements
- **multi_waves** - Complex wave interactions

### Vintage & Classic
- **vintage_leather** - Rich leather texture with classic styling
- **textile_corduroy** - Fabric texture with warm tones
- **casual_denim** - Denim texture for casual projects
- **architect_concrete** - Minimalist concrete aesthetic

### Colorful & Playful
- **vaporwave** - Retro pink-blue aesthetic with 80s vibes
- **sunny_morning** - Bright, cheerful morning colors
- **sunset_stream** - Warm sunset gradients
- **sunset_stream_dark** - Dark variant of sunset theme
- **orange_blue** - Vibrant orange-blue contrast
- **energy_orange** - High-energy orange themes
- **pastel_leaf** - Soft pastel colors with nature themes

### Minimal & Clean
- **flat_minimal** - Ultra-clean flat design
- **perfect_circles** - Simple geometric circle patterns
- **diagonal_stripes** - Clean diagonal line patterns
- **diagonal_stripes_bold** - Bold version of diagonal stripes
- **writer_beige** - Minimalist beige for writing projects

### Accessible Design
- **accessible_blue_orange** - High contrast blue-orange combination
- **accessible_purple_yellow** - High contrast purple-yellow combination
- **bw_high_contrast** - Black and white high contrast design

### Specialized Themes
- **edu_blue** - Educational blue theme for learning projects
- **healthcare_mint** - Calming mint green for healthcare
- **green_soft** - Soft green for wellness projects
- **auto_color** - Automatically adapts colors based on your icon

## Preset Categories

### By Use Case
- **Startups:** modern_blue, purple_tech, cyber_yellow
- **Portfolios:** dark_portfolio, geometric_chaos, blob_garden
- **Open Source:** github_pro, modern_blue, accessible_blue_orange
- **Creative:** vaporwave, geometric_chaos, polygon_constellation
- **Professional:** business_green, fintech_gold, architect_concrete
- **Education:** edu_blue, accessible_blue_orange, flat_minimal
- **Gaming:** cyber_yellow, neon_retro, matrix_grid

### By Color Scheme
- **Blue Themes:** modern_blue, edu_blue, accessible_blue_orange
- **Green Themes:** business_green, nature_breeze, healthcare_mint
- **Purple Themes:** purple_tech, accessible_purple_yellow
- **Warm Themes:** sunset_stream, energy_orange, sunny_morning
- **Dark Themes:** dark_portfolio, matrix_grid, cyber_yellow

### By Design Style
- **Minimal:** flat_minimal, perfect_circles, architect_concrete
- **Geometric:** geometric_chaos, polygon_constellation, layered_shapes
- **Organic:** blob_garden, organic_blobs, nature_breeze
- **Textured:** vintage_leather, textile_corduroy, casual_denim
- **Gradient:** modern_blue, sunset_stream, vaporwave

## Customizing Presets

You can modify any preset by adding additional parameters:

```bash
# Add accent color to any preset
python banner_maker.py --preset modern_blue --title "My Project" --accent "red"

# Modify intensity
python banner_maker.py --preset geometric_chaos --title "My Project" --intensity "high"

# Add rounded corners
python banner_maker.py --preset vintage_leather --title "My Project" --rounded "25"

# Combine with custom elements
python banner_maker.py --preset ocean_waves --title "My Project" --texture "grain:20"
```

## Creating Your Own Presets

Presets are JSON files located in `core/presets/`. Each preset defines:
- Background colors and gradients
- Pattern configurations
- Shape elements
- Texture effects
- Visual effects
- Typography settings

To create a custom preset:
1. Copy an existing preset from `core/presets/`
2. Modify the JSON configuration
3. Save with a new name
4. Use with `--preset your_preset_name`

## Technical Details

- **Total Presets:** 43 carefully designed templates
- **Format:** JSON configuration files
- **Location:** `core/presets/*.json`
- **Validation:** Built-in parameter validation
- **Extensibility:** Easy to add new presets

## Need Help?

```bash
# See all available presets
python banner_maker.py --help

# Learn the CLI equivalent of any preset
python banner_maker.py --learn preset_name

# Generate examples of all presets
python banner_maker.py --demo-set
```

---

*Each preset is designed to showcase different aspects of Banner Maker's capabilities while providing ready-to-use professional designs.*