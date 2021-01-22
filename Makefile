SHELL := /bin/bash

test:
	python -m unittest discover tests
.PHONY: test

dist:
	rm -rf build dist SeismicFoldDbGis.egg-info
	python3 setup.py sdist bdist_wheel
.PHONY: dist

dist-upload-test:
	python3 -m twine upload --repository testpypi dist/*
.PHONY:dist-upload-test

dist-upload:
	python3 -m twine upload --repository pypi dist/*
.PHONY: dist-upload