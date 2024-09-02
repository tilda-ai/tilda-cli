#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='tilda',
    version='0.0.1',
    python_requires='>=3.12',
    packages=find_packages(exclude=('tests',)),
    package_data={
        '': ['*.jinja2'], # If any package contains *.jinja2 files, include them.
    },
    include_package_data=True,
    install_requires=[
        'keyring==25.2.1',
        'inquirerpy==0.3.4',
        'argparse==1.4.0',
        'logging==0.4.9.6',
        'jinja2==3.1.3',
        'openai==1.21.2',
        'toml==0.10.2',
        'watchdog==4.0.0',
        'pathspec==0.12.1',
        'rich==13.7.1',
        'build==1.2.1',
        'prompt-toolkit==3.0.43',
        'jsonschema==4.22.0',
    ],
    entry_points={
        'console_scripts': [
            'tilda=src.cli:main',
        ],
    },
    author='tilda.ai',
    url='http://github.com/tilda.ai/tilda',
    description='The AI CLI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)