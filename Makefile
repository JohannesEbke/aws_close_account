.PHONY: install test release

install:
	python setup.py install

test:
	pip install --upgrade flake8 yapf
	python setup.py install
	aws_close_account --help
	flake8 aws_close_account
	yapf -d -r aws_close_account/

release: test
	rm -rf dist build
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
