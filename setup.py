from setuptools import find_packages
from setuptools import setup


setup(
    name='unittest-hooks',
    description='unittest',
    url='https://github.com/pre-commit/pre-commit-hooks',
    version='1.0.0',

    author='Nanthakumar Loganathan',
    author_email='splnanthakumar@gmail.com',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages=find_packages(exclude=('tests*', 'testing*')),
    install_requires=[
        # quickfix to prevent pycodestyle conflicts
        'invoke==0.11.1',
    ]
)