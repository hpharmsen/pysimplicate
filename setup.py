import setuptools
from pathlib import Path

scriptpath = Path(__file__).resolve().parent
with open(scriptpath / "README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open(scriptpath / "version.txt", "r") as fh:
    version = fh.read()

setuptools.setup(
    name="pysimplicate",
    version=version,
    author="Hans-Peter Harmsen",
    author_email="hph@oberon.nl",
    description="Python wrapper for the Simplicate API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hpharmsen/pysimplicate",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
