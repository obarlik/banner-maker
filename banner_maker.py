# banner_maker.py
"""
Banner Maker - Main CLI Application
Professional banner generation tool with modern CLI interface.
"""

import sys
from banner.pipeline import generate_banner, BannerConfig
from demo.demo_set import generate_demo_set
from core.cli_parser import get_banner_config_from_cli, parse_new_cli_arguments


def convert_config_to_dict(config):
    """Convert BannerConfig to dictionary for demo_set compatibility."""
    args_dict = {}
    for field_name in BannerConfig.__dataclass_fields__.keys():
        if hasattr(config, field_name):
            args_dict[field_name] = getattr(config, field_name)
    return args_dict


def show_config_debug(config):
    """Show configuration for debugging purposes."""
    print("\n[CLI Configuration]:")
    config_dict = {}
    for field_name in BannerConfig.__dataclass_fields__.keys():
        if hasattr(config, field_name):
            value = getattr(config, field_name)
            if value is not None:
                config_dict[field_name] = value
    
    for k, v in config_dict.items():
        print(f"  {k}: {v}")
    print()


def main():
    """Main application entry point."""
    try:
        # Parse CLI arguments and get configuration
        config = get_banner_config_from_cli()
        raw_config = parse_new_cli_arguments()
        
        # Handle demo generation
        if raw_config.get('demo', False):
            print("Generating demo banner set...")
            args_dict = convert_config_to_dict(config)
            args_dict['demo'] = True
            generate_demo_set(args_dict)
            print("Demo generation completed successfully!")
            return
        
        # Show configuration for debugging (only if verbose)
        if config.verbose:
            show_config_debug(config)
        
        # Generate banner
        print(f"Generating banner: {config.title}")
        generate_banner(config)
    
    except FileNotFoundError as e:
        print(f"\nError: File not found: {e}")
        print("Check that all file paths are correct and files exist.")
        sys.exit(1)
    except PermissionError as e:
        print(f"\nError: Permission denied: {e}")
        print("Check file permissions and try running as administrator if needed.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except ImportError as e:
        print(f"\nError: Missing dependency: {e}")
        print("Install dependencies with: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        print("For help, run: python banner_maker.py --help")
        print("If this persists, please report at: https://github.com/obarlik/banner-maker/issues")
        sys.exit(1)


def cli_main():
    """Entry point for console script."""
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        print("For help, run: python banner_maker.py --help")
        sys.exit(1)


if __name__ == "__main__":
    main()
