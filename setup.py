from setuptools import setup, find_packages

setup(
        name='tfl_requests', 
        #version='0.1',
        packages=find_packages(),
        package_data = {
            '' : ['*.txt']
            },
        install_requires=['python-dateutils'],
        author='anna', 
        author_email='iria.a.pantazi@gmail.com',
        description='utility for tfl line status',
        keywords='tfl status',
        url='https://github.com/iriapantazi/tfl_requests', # project homepage
        )
