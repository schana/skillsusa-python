from setuptools import setup, find_packages

setup(
    name='skillsusa',
    version='0.1',
    packages=find_packages(exclude=['test', 'test.*', '*.test']),
    install_requires=['pygame'],
    tests_require=['pytest', 'pytest-subtests', 'pytest-xdist'],
    setup_requires=['pytest-runner'],
    test_suite='pytest',
    url='',
    license='',
    author='Nathaniel Schaaf',
    author_email='',
    description=''
)
