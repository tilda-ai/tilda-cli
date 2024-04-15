from setuptools import setup, find_packages

setup(
    name='tilda',
    version='0.0.1',
    python_requires='==3.12.2',
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'argparse==1.4.0',
        'logging==0.4.9.6',
    ],
    entry_points={
        'console_scripts': [
            'tilda=src.tilda:main',
        ],
    },
    author='rkyd',
    author_email='email@example.com',
    url='http://github.com/tilda/cli',
    description='The AI CLI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)