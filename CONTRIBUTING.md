# Contributing to GitHub Banner Maker

Thank you for your interest in contributing to GitHub Banner Maker! This document provides guidelines and information for contributors.

## Development Philosophy

This project follows **DRY + KISS principles**:
- **DRY (Don't Repeat Yourself)**: Eliminate code duplication through centralized utilities
- **KISS (Keep It Simple, Stupid)**: Maintain simple, functional code over complex architecture patterns
- **Global-first**: English-only codebase for international collaboration

## Code Organization

### Core Utilities (`core/`)
- `color_utils.py` - Color parsing, contrast, and conversion functions
- `geometry_utils.py` - Geometric calculations, gradients, and shape utilities  
- `layer_utils.py` - Image composition and layer management
- `font_utils.py` - Font loading, sizing, and text measurement
- `config_utils.py` - Configuration parameter extraction and validation
- `constants.py` - Centralized constants and magic numbers

### Main Modules (`banner/`)
- `pipeline.py` - Main banner generation pipeline
- `textures.py` - Texture generation and effects
- `motifs.py` - Pattern and motif generation
- `overlays.py` - Overlay effects and compositions
- `shapes.py` - Shape drawing and effects

## Getting Started

### Prerequisites
- Python 3.8+
- PIL/Pillow
- NumPy
- Basic understanding of image processing

### Development Setup
1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/banner-maker.git`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `python banner_maker.py --help`

## Contributing Guidelines

### Code Style
- **No complex architecture patterns** (SOLID, Clean Architecture, plugins)
- **Functional programming** preferred over object-oriented complexity
- **English-only** comments, variable names, and documentation
- **Consistent naming** following existing patterns
- **DRY principles** - use core utilities instead of duplicating code

### Before You Code
1. Check existing issues and pull requests
2. Create an issue to discuss major changes
3. Follow the established patterns in core utilities
4. Test your changes with different banner configurations

### Making Changes

#### Adding New Features
- Add core functionality to appropriate `core/` utility module
- Use existing utilities instead of creating duplicates
- Update constants in `core/constants.py` if needed
- Add examples to documentation

#### Bug Fixes
- Identify root cause and fix in the appropriate utility module
- Ensure fix doesn't break existing functionality
- Test with various configurations

#### Refactoring
- Follow DRY principles by centralizing common code
- Keep changes simple and focused
- Update imports to use centralized utilities

### Code Quality
- **Import organization**: Use centralized utilities from `core/`
- **Error handling**: Graceful fallbacks and informative messages
- **Documentation**: Clear docstrings for public functions
- **Constants**: Use `core/constants.py` instead of magic numbers

### Pull Request Process
1. **Create feature branch**: `git checkout -b feature/your-feature-name`
2. **Make focused commits**: One logical change per commit
3. **Test your changes**: Verify banner generation works
4. **Update documentation**: Update README if needed
5. **Submit pull request**: Use the PR template

### Pull Request Requirements
- [ ] Code follows DRY + KISS principles
- [ ] Uses existing core utilities instead of duplicating code
- [ ] English-only code and comments
- [ ] No complex architecture patterns introduced
- [ ] Backwards compatible (unless major version)
- [ ] Documentation updated if needed

## Types of Contributions

### Welcome Contributions
- **Bug fixes** - Especially cross-platform compatibility
- **New textures** - Additional texture generation algorithms
- **New motifs** - Creative pattern generators  
- **Font improvements** - Better font discovery and fallbacks
- **Documentation** - Examples, tutorials, API docs
- **Performance** - Optimization without complexity

### Discouraged Contributions
- Complex architecture refactors (plugins, dependency injection, etc.)
- Over-engineered solutions
- Non-English code or comments
- Breaking changes without clear benefits

## Code Examples

### Adding a New Utility Function
```python
# core/color_utils.py
def your_new_function(color, param):
    """
    Clear description of what this does.
    
    Args:
        color: Color input (hex, rgb tuple, etc.)
        param: Parameter description
        
    Returns:
        Processed color or result
    """
    # Implementation
    return result
```

### Using Core Utilities
```python
# In any module
from core.color_utils import parse_color, get_contrast_color
from core.constants import DEFAULT_TEXT_COLOR

# Use centralized functions
color = parse_color("#FF0000")
contrast = get_contrast_color(color)
```

## Questions and Support

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions
- **Documentation**: Check README.md and CLAUDE.md first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make GitHub Banner Maker better! 🎨