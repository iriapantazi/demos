#! /usr/bin/env python
from setuptools import setup, find_packages

setup(
        name='tfl_requests', 
        version='0.0.1',
        packages=find_packages(),
        #package_dir={'' : 'src'},
        scripts=[
            'src/trainsLinesStatus.py',
            ],
        install_requires='requirements.txt',
        package_data = {
            '' : ['*.txt', '*.md'],
            },
        # metadata to display on pypi
        author='Iria Pantazi', 
        author_email='iria.a.pantazi@gmail.com',
        description='Utility displaying status of tfl lines',
        keywords='tfl status',
        url='https://github.com/iriapantazi/tfl_requests',
        )
