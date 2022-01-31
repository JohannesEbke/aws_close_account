#!/bin/bash
set -eux

rm -rf dist build
pip install --upgrade flake8 yapf twine
python setup.py install
aws_close_account --help
flake8 aws_close_account
yapf -d -r aws_close_account/
python3 setup.py sdist bdist_wheel
twine upload dist/*

