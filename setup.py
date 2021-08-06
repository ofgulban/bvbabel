"""bvbabel setup.

To install, using the command line do:
    pip install -e /path/to/bvbabel

Notes for PyPI:
python setup.py sdist upload -r pypitest
python setup.py sdist upload -r pypi

"""

from setuptools import setup

VERSION = '0.1.0'

setup(name='bvbabel',
      version=VERSION,
      description='A lightweight Python library for reading and writing BrainVoyager file formats.',
      url='https://github.com/ofgulban/bvbabel',
      download_url=('https://github.com/ofgulban/bvbabel/archive/'
                    + VERSION + '.tar.gz'),
      author='Omer Faruk Gulban',
      author_email='gulban@brainvoyager.com',
      license='MIT',
      packages=['bvbabel'],
      install_requires=['numpy'],
      zip_safe=False)
