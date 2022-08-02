# Importing the required modules.
from setuptools import setup, find_packages
import codecs
import os

# Defiining the setup parameters.
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

with codecs.open(os.path.join(here, 'requirements.txt'), encoding="utf-8") as f:
    lines = (x.strip() for x in f.read().splitlines())
    requirements = [x for x in lines if x and not x.startswith("#")]

VERSION = '2022.8.2'
DESCRIPTION = 'An asynchronous Python wrapper for the Minecraft Server Status API.'

# Setup.
setup(
    name='api.mcsrvstat.py',
    version=VERSION,
    author='HitBlast',
    author_email='<hitblastlive@gmail.com>',
    url='https://github.com/hitblast/api.mcsrvstat.py',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.10',
    keywords=['python', 'minecraft', 'mcsrvstat'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.10',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ],
    entry_points='''
        [console_scripts]
        mcsrvstat=mcsrvstat.cli:cli
    '''
)
