"""
Setup script for the Evolutionary Simulation project.
"""

from setuptools import setup, find_packages

with open("docs/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="evosim",
    version="0.1.0",
    author="Zen Garden",
    author_email="zengarden.thesisdev@gmail.com",
    description="Educational Survival Simulation Using Evolutionary Algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Meixii/evosim",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black>=22.0.0",
            "flake8>=4.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
        ],
        "enhanced": [
            "pandas>=1.4.0",
            "seaborn>=0.11.0",
            "scipy>=1.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "evosim=src.main:main",
        ],
    },
)
