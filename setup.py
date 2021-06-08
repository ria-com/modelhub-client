import os
import setuptools

# get project long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# get project version
with open("version.txt", "r", encoding="utf-8") as fh:
    version = fh.read()

# get project requirements list
with open("requirements.txt", "r", encoding="utf-8") as fh:
    packages = fh.read().split("/n")

setuptools.setup(
    name="modelhub-client",
    version=version,
    author='RIA.com',
    author_email='dmytro.probachay@ria.com',
    description="RIA ModelHub tools package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.ria.com/neural/ria-modelhub-tools.git",
    packages=setuptools.find_packages(),
    install_requires=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
