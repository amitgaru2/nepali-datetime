from setuptools import setup, find_packages

from nepali_datetime import __version__, __author__

with open('README.md', encoding='utf-8') as readme_file:
    README = readme_file.read()

setup(
    name="nepali-datetime",
    version=__version__,
    description="Datetime module that operates on top of Bikram Sambat Date & Nepal Time.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/amitgaru2/nepali-datetime",
    author=__author__,
    author_email="amitgaru2@gmail.com",
    license="MIT",
    packages=find_packages(exclude=("tests", "docs")),
    keywords=['nepali', 'bs', 'b.s', 'date', 'datetime', 'time', 'timezone', 'nepal', 'bikram', 'sambat', 'samvat',
              'nepali-date', 'nepali-datetime', 'nepal-time', 'npt', 'nepal-timezone'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
