# Copyright (C) 2022 Nusret Ipek

# Import setuptools

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup
    
# Setup parameters

DISTNAME = "HierarchiaPy"
VERSION = "0.2.3"
AUTHOR = "Nusret Ipek"
AUTHOR_EMAIL ="Nusret.Ipek@UGent.be"

DESC = "HierarchiaPy: statistical package to derive hiearchy from social interactions"
with open("README.md", "r") as f:
    LONG_DESC = f.read()
LONG_DESC_TYPE = "text/markdown"

URL = "https://github.com/nusretipek/HierarchiaPy"
LICENSE = 'MIT'
INSTALL_REQUIRES = [
    "numpy>=1.19",
    "scipy>=1.7",
    "pandas>=1.0",
    "matplotlib>=3.0.2",
    "networkx>=2.0"
]

PACKAGES=["HierarchiaPy", "HierarchiaPy/methods", "HierarchiaPy/linearity"]
CLASSIFIERS = [
              "Development Status :: 2 - Pre-Alpha",
              "Programming Language :: Python :: 3",
              "Programming Language :: Python :: 3 :: Only",
              "Programming Language :: Python :: 3.7",
              "Programming Language :: Python :: 3.8",
              "Programming Language :: Python :: 3.9",
              "License :: OSI Approved :: MIT License",
              "Topic :: Sociology",
              "Intended Audience :: Science/Research",
              "Operating System :: Microsoft :: Windows",
              "Operating System :: Unix",
              "Operating System :: MacOS",
]

# Setup

if __name__ == "__main__":
    
    setup(name=DISTNAME,
          version=VERSION,
          author=AUTHOR,
          author_email=AUTHOR_EMAIL,
          description=DESC,
          long_description=LONG_DESC,
          long_description_content_type=LONG_DESC_TYPE,
          license=LICENSE,
          packages=PACKAGES,
          url=URL,
          download_url=URL,
          install_requires=INSTALL_REQUIRES,
          classifiers=CLASSIFIERS
         )
