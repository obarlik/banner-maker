# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Core utility modules for DRY architecture
- Centralized color utilities (`core/color_utils.py`)
- Centralized geometry utilities (`core/geometry_utils.py`) 
- Centralized layer utilities (`core/layer_utils.py`)
- Centralized font utilities (`core/font_utils.py`)
- Centralized configuration utilities (`core/config_utils.py`)
- Centralized constants (`core/constants.py`)
- Comprehensive CLAUDE.md documentation for developers
- DRY + KISS development principles

### Changed
- Refactored codebase to eliminate code duplication
- Consolidated duplicate functions across modules
- Updated all imports to use centralized utilities
- Converted Turkish comments and text to English for global use

### Fixed
- Windows encoding issues with Turkish characters
- Import references to use centralized utilities
- Code duplication across multiple modules

## [1.0.0] - 2024-01-XX

### Added
- Initial GitHub Banner Maker implementation
- PIL-based banner generation pipeline
- Support for multiple textures (noise, grain, organic crumpled paper, concrete)
- Support for multiple motifs (dots, lines, circles, squares, stars, etc.)
- Support for multiple overlays and shapes
- Configurable parameters via JSON and command line
- Supersampling support for high-quality output
- Font loading with cross-platform compatibility
- Border and corner radius support
- Demo generation functionality
- Comprehensive README with examples

### Technical Features
- Modular architecture with separate concerns
- Configuration via dataclass with parameter validation
- Cross-platform font discovery
- Color parsing and contrast calculation
- Gradient generation (vertical, horizontal, diagonal, radial)
- Layer-based composition system
- Command-line interface with argparse

---

## Release Notes

### Version Numbering
This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backwards compatible manner  
- **PATCH** version for backwards compatible bug fixes

### Support
For questions, issues, or contributions, please visit the [GitHub repository](https://github.com/obarlik/banner-maker).