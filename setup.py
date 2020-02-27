from setuptools import setup, find_packages

setup(
    name='skillsusa',
    version='1.0',
    packages=find_packages(),
    install_requires=['pygame'],
    entry_points={'console_scripts': ['snake = game.runner:main']},
    url='github.com/schana/skillsusa',
    license='License :: OSI Approved :: Apache Software License',
    author='Nathaniel Schaaf',
    author_email='nathaniel.schaaf@gmail.com',
    description='Code for contest to build an ai for the game of snake'
)
