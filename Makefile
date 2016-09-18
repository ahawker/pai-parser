.PHONY: test-install test tox travis-install travis-script clean-pyc

test-install:
	pip install -q -r requirements/test.txt

test: test-install
	py.test tests

tox:
	tox

travis-install:
	pip install -q -r requirements/travis.txt

travis-script: travis-install tox

clean-pyc:
	find . -name '__pycache__' -type d -exec rm -r {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
