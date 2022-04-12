from setuptools import setup

setup(
    name='korg',
    version='0.2.0',    
    description='Attacker synthesis for distributed protocols',
    url='https://github.com/maxvonhippel/AttackerSynthesis',
    author='Max von Hippel and Cole Vick',
    author_email='vonhippel.m@northeastern.edu',
    license='BSD 2-clause',
    packages=['korg'],
    install_requires=['argparse',],

    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8.5',
    ],
)