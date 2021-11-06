
from distutils.core import setup


setup(
    name='gvarplot',
    description='Utilities for plotting gvars and lsqfits.',
    author='Evan Berkowitz',
    author_email='git@evanberkowitz.com',

    # pip:
    install_requires=['gvar>=11.9.4'],
    requires=['gvar (>=11.9.4)', 'lsqfit'],
    license='GPLv3+',
    classifiers = [
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        ]
)
