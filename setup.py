import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysimplicate-pkg", # Replace with your own username
    version="0.1.0",
    author="Hans-Peter Harmsen",
    author_email="hph@oberon.nl",
    description="Python wrapper for the Simplicate API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hpharmsen/pysimplicate",
    packages=setuptools.find_packages(),
install_requires=[
          'requests',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: The Unlicense",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)