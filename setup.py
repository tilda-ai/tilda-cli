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
        'inquirerpy==0.3.4',
        'argparse==1.4.0',
        'logging==0.4.9.6',
        'anthropic==0.25.5',
        'google-generativeai==0.5.1',
        'groq==0.5.0',
        'jinja2==3.1.3',
        'mistralai==0.1.8',
        'ollama==0.1.7',
        'openai==1.21.2',
        'sqlmodel==0.0.16',
        'tiktoken==0.6.0',
        'toml==0.10.2',
    ],
    entry_points={
        'console_scripts': [
            'tilda=src.tilda:main',
        ],
    },
    author='tilda.ai',
    url='http://github.com/tilda.ai/tilda',
    description='The AI CLI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)