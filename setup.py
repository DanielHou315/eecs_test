from setuptools import setup, find_packages
setup(
    name='eecs_test',
    version='0.1.0',
    author='Huaidian Hou',
    author_email='danielhou315@gmail.com',
    description='A simple test utility for U-M EECS courses',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)