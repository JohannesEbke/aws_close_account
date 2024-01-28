from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aws_close_account',
    version='0.3.2',
    description='Programmatically close an AWS account using Selenium ',
    long_description=long_description,
    url='https://github.com/JohannesEbke/aws_close_account',
    author='Johannes Ebke',
    author_email='johannes@ebke.org',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='aws account selenium',
    packages=['aws_close_account'],
    install_requires=['selenium>=4.1.0'],
    entry_points={
        'console_scripts': [
            'aws_close_account=aws_close_account.__main__:main',
            'aws-close-account=aws_close_account.__main__:main',
        ],
    },
)
