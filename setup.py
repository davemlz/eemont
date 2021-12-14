import io
import os
import re

from setuptools import find_packages, setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


setup(
    name="eemont",
    version="0.3.0",
    url="https://github.com/davemlz/eemont",
    license="MIT",
    author="David Montero Loaiza",
    author_email="dml.mont@gmail.com",
    description="A Python package that extends Google Earth Engine",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests",), include=["eemont", "eemont.*"]),
    package_data={"eemont": ["data/*.json"]},
    install_requires=[
        "beautifulsoup4",
        "earthengine-api",
        "ee_extra>=0.0.9",
        "numpy",
        "pandas",
        "python-box",
        "geopy",
        "requests",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
