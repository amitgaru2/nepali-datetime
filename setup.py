from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    README = readme_file.read()

setup(
    name="nepali-datetime",
    version="1.0.2",
    description="datetime module that operates on B.S",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/arneec/nepali-datetime",
    author="Amit Garu",
    author_email="amitgaru2@gmail.com",
    license="MIT",
    packages=find_packages(exclude=("tests", "docs")),
    keywords=['nepali', 'bs', 'b.s', 'date', 'datetime', 'nepal', 'bikram', 'sambat', 'samvat', 'calendar',
              'nepali-calendar', 'nepali-date', 'nepali-datetime', 'nepali_date', 'nepali_datetime'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
