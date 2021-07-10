import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="eemont",
    version="0.2.4",
    url="https://github.com/davemlz/eemont",
    license='MIT',

    author="David Montero Loaiza",
    author_email="dml.mont@gmail.com",

    description="A Python package that extends Google Earth Engine",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',),include=["eemont", "eemont.*"]),
    
    package_data={'eemont': ['data/*.json']},
    
    install_requires=['earthengine-api','numpy','pandas','python-box','geopy','requests'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
