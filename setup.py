"""
setuptools file for AnchorHub
Copyright 2016. Sam Abrahams
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import anchorhub

here = path.abspath(path.dirname(__file__))

# Want this to work, but it's breaking the build right now
# Will fix after finishing refactoring
#with open(path.join(path.dirname(__file__), 'anchorhub/VERSION'), 'rb') as f:
#    version = f.read().decode('ascii').strip()
#    f.close()

# Get the long description from the README file
with open(path.join(path.dirname(__file__), 'PYPI.rst'), 'rb') as f:
    long_description = f.read().decode('ascii')
    f.close()

setup(
    name='anchorhub',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=anchorhub.__version__,

    description='Easily utilize GitHub\'s automatically generated anchors within and across Markdown documents',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/samjabrahams/anchorhub',

    # Author details
    author='Sam Abrahams',
    author_email='sam@samabrahams.com',

    # Choose your license
    license='Apache 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Pre-processors',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='markdown anchor links processing',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=('*.tests', '*.tests.*', 'tests.*',
                                    'tests')),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['nose'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={},

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={'anchorhub': ['VERSION']},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'anchorhub=anchorhub.main:main'
        ]
    },
)