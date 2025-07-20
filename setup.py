from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="banner-maker",
    version="1.0.0",
    author="obarlik",
    author_email="obarlik@codechu.com",
    description="A powerful, customizable Python tool to generate modern banners for GitHub projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/obarlik/banner-maker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "advanced": ["scipy>=1.7.0", "matplotlib>=3.3.0"],
    },
    entry_points={
        "console_scripts": [
            "banner-maker=banner_maker:cli_main",
        ],
    },
    keywords="github banner image generation pillow graphics",
    project_urls={
        "Bug Reports": "https://github.com/obarlik/banner-maker/issues",
        "Source": "https://github.com/obarlik/banner-maker",
        "Documentation": "https://github.com/obarlik/banner-maker#readme",
    },
) 