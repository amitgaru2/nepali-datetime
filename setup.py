from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    README = readme_file.read()

setup(
    name="nepali-datetime",
    version="1.0.3",
    description="datetime module that operates on bikram sambat & nepal time",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/dxillar/nepali-datetime",
    author="Amit Garu",
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
