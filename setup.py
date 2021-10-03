from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
from ccg import __version__

setup(
    name='ccg',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=__version__,
    packages=find_packages(include=["ccg", "ccg.*"]),
    url='https://github.com/polfeliu/CCG',
    license='Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)',
    author='Pol Feliu Cuberes',
    author_email='feliupol@gmail.com',
    keywords='ccg c cpp codegen generation',
    description='C/C++ code generation framework'
)
