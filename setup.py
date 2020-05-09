from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    README = readme_file.read()

setup(
    name="nepali-date",
    version="2.0.5",
    description="Nepali Date API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/arneec/nepali-date",
    author="Amit Garu",
    author_email="amitgaru2@gmail.com",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    keywords=['Nepali', 'BS', 'B.S', 'Date', 'Nepal', 'Bikram', 'Sambat',
              'Year', 'Month', 'Day', 'calendar', 'nepali-calendar', 'nepali-date'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
