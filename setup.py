from setuptools import setup, find_packages

setup(
    name="solana_fm",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["httpx", "pandas"],
    description="Module for work Solscan API",
    author="Tsunami43",
    url="https://github.com/Tsunami43/solscan",
)
