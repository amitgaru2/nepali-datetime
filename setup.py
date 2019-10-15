from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    README = readme_file.read()

setup(
    name="nepali-date",
    version="2.0.2",
    description="Nepali Date API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/arneec/nepali-date",
    author="Amit Garu",
    author_email="amitgaru2@gmail.com",
    license="MIT",
    packages=find_packages(),
    keywords=['Nepali', 'BS', 'B.S', 'Date', 'Nepal', 'Bikram', 'Sambat',
              'Year', 'Month', 'Day'],
    include_package_data=True
)
