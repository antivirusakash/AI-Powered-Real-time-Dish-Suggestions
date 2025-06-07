"""
Setup configuration for AI Powered Real-time Dish Suggestions
AI Powered Real-time dish suggestions with portion sizes for accurate calorie tracking
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-powered-dish-suggestions",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI Powered Real-time dish suggestions with portion sizes for accurate calorie tracking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antivirusakash/AI-Powered-Real-time-Dish-Suggestions",
    project_urls={
        "Bug Tracker": "https://github.com/antivirusakash/AI-Powered-Real-time-Dish-Suggestions/issues",
        "Documentation": "https://github.com/antivirusakash/AI-Powered-Real-time-Dish-Suggestions#readme",
        "Source": "https://github.com/antivirusakash/AI-Powered-Real-time-Dish-Suggestions",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Flask",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "isort>=5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-powered-dish-suggestions=app:app",
        ],
    },
    keywords=[
        "ai", 
        "calorie-tracking", 
        "food-logging", 
        "nutrition", 
        "azure-openai", 
        "real-time-suggestions", 
        "portion-sizes",
        "diet-tracking",
        "fitness",
        "health",
        "flask",
        "machine-learning"
    ],
    include_package_data=True,
    zip_safe=False,
) 