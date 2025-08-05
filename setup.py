#!/usr/bin/env python3
"""Setup script for GE HealthCare Intelligent Data Store SDK."""

from setuptools import setup, find_packages
import os

# Read the README file
current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gehc-ids-sdk",
    version="1.0.0",
    author="GE HealthCare",
    author_email="ai-fabric@gehealthcare.com",
    description="Python SDK for GE HealthCare Intelligent Data Store API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gehealthcare/ids-sdk-python",
    packages=find_packages(exclude=["tests*", "examples*"]),
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
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Database",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "examples": [
            "jupyter>=1.0.0",
            "matplotlib>=3.5.0",
            "pandas>=1.5.0",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/gehealthcare/ids-sdk-python/issues",
        "Source": "https://github.com/gehealthcare/ids-sdk-python",
        "Documentation": "https://gehealthcare.github.io/ids-sdk-python/",
    },
    keywords="gehealthcare, ai, vector-store, prompt-store, embeddings, rag",
    license="MIT",
    zip_safe=False,
    include_package_data=True,
)