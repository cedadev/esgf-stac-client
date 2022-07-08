from setuptools import setup, find_packages
from os.path import basename, splitext
from glob import glob

setup(
    name="esgf-stac-client",
    version="0.0",
    description=(
        "A Python client to access ESGF STAC data"
    ),
    author="Mahir Rahman",
    author_email="kazi.mahir@stfc.ac.uk",
    url="https://github.com/cedadev/esgf-stac-client",
    packages=find_packages(exclude=("tests",)),
    py_modules=[splitext(basename(path))[0] for path in glob("pystac_client/*py")],
    python_requires=">=3.8",
    dependency_links=[
        "https://github.com/cedadev/pystac.git@asset-search",
        "https://github.com/cedadev/pystac-client.git@asset-search",
    ],
    license="BSD 2-Clause License",
)
