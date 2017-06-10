from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='forte-fives',
    version='0.1.0',
    description='The not-so-known game of 45s',
    long_description=readme,
    author='Luiz Carvalho',
    author_email='luizcarvalho85@gmail.com',
    url='https://github.com/lcarva/forte-fives',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points = {
        'console_scripts': ['forte-fives=forte_fives.cli:main']
    },
)
