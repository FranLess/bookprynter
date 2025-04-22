from setuptools import setup

setup(
    name='bookprynter',
    version='0.1.0',
    py_modules=['bookprynter'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'bookprynter=bookprynter:cli',
        ],
    },
)