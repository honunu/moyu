"""
Moyu CLI 安装配置
"""
from setuptools import setup, find_packages

setup(
    name="moyu",
    version="0.1.0",
    description="摸鱼命令行工具 - 让摸鱼变得更专业",
    author="摸鱼大师",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "moyu=moyu_cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
