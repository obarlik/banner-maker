# Banner Maker Package
try:
    from .banner_maker import main, cli_main
except ImportError:
    from banner_maker import main, cli_main

__version__ = "0.1.8"
__author__ = "Onur Barlik"