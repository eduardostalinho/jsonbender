from setuptools import setup, find_packages
from jsonbender import __version__


setup(
    name='JSONBender',
    version=__version__,
    description='Library for transforming dicts.',
    packages=find_packages(),
)

