import pathlib
import random
from os import path

from setuptools import find_packages, setup

from ccg import __version__

this_directory = path.abspath(path.dirname(__file__))
long_description = pathlib.Path(path.join(this_directory, "README.md")).read_text(encoding="utf-8")

if "dev" in __version__:
    # Development versions cache busting
    __version__ += str(random.randint(0, 0xFFFFFFFF))

setup(
    name="ccg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=__version__,
    packages=find_packages(include=["ccg", "ccg.*"]),
    url="https://github.com/polfeliu/CCG",
    license="Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)",
    author="Pol Feliu Cuberes",
    author_email="feliupol@gmail.com",
    keywords="ccg c cpp codegen generation",
    description="C/C++ code generation framework",
)
