"""Setup script for S42 Euler sum package."""

from setuptools import setup, find_packages
import os

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh 
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="s42-euler-sum",
    version="1.0.0",
    author="Keenan Williams",
    author_email="your-email@example.com",
    description="Exact closed-form identities for the S₄,₂(x) Euler sum",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/keewillidevnet/S42-omega2-reproducibility",
    project_urls={
        "Bug Tracker": "https://github.com/keewillidevnet/S42-omega2-reproducibility/issues",
        "Documentation": "https://github.com/keewillidevnet/S42-omega2-reproducibility/blob/main/docs/API.md",
        "Paper": "https://github.com/keewillidevnet/S42-omega2-reproducibility/blob/main/docs/paper.pdf",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "gpu": ["torch>=2.0.0"],
        "symbolic": ["sympy>=1.12"],
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.4.0",
        ],
        "docs": [
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
        "notebooks": [
            "jupyter>=1.0.0",
            "ipykernel>=6.25.0",
            "ipywidgets>=8.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "s42-benchmark=s42.cli:benchmark_cli",
            "s42-verify=s42.cli:verify_cli",
            "s42-evaluate=s42.cli:evaluate_cli",
        ],
    },
    include_package_data=True,
    package_data={
        "s42": ["data/**/*.json", "data/**/*.yaml"],
    },
    keywords="euler sums, polylogarithms, PSLQ, special functions, high-precision arithmetic",
    zip_safe=False,
)
