from pathlib import Path
from setuptools import setup, find_packages

AUTHOR_NAME = 'Chris Hoyer'
AUTHOR_EMAIL = 'info@chrishoyer.de'

ROOT = Path(__file__).resolve().parent

# get latest version from source code
def get_version():
    v = {}
    for line in (ROOT / "src" / "pyaltiumlib" / "__init__.py").read_text().splitlines():
        if line.strip().startswith('__version__'):
            exec(line, v)
            return v['__version__']
    raise IOError('__version__ string not found')

# get description from readme.md
def get_description():  
    long_description = ""
    with open("README.md", "r") as f:
        long_description = f.read()
    return long_description    

setup(name='pyaltiumlib',
      version=get_version(),
      description='PyAltiumLib is a tool to read Altium Designer library files.',
      url='https://github.com/ChrisHoyer/pyAltiumLib.git',
      author=AUTHOR_NAME,
      author_email=AUTHOR_EMAIL,
      packages=find_packages(where="src"),
      install_requires=['olefile>=0.47', 'svgwrite>=1.4.3'],
      package_dir={"": "src"},
      python_requires=">=3.7",
      long_description=get_description(),
      long_description_content_type="text/markdown",    
      )