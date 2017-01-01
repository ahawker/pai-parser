.PHONY: test-install test tox-install tox travis-install travis-script clean-pyc

test-install:
	pip install -q -r requirements/test.txt

test: test-install
	py.test tests

tox-install:
	pip install -q -r requirements/tox.txt

tox: tox-install
	tox

coveralls-install:
	pip install -q -r requirements/coveralls.txt

travis-install: coveralls-install
	pip install -q -r requirements/travis.txt

travis-script: travis-install tox

clean-pyc:
	find . -name '__pycache__' -type d -exec rm -r {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

bump-patch:
	bumpversion patch

bump-minor:
	bumpversion minor

bump-major:
	bumpversion major

git-push-with-tags:
	git push
	git push --tags

push-patch: bump-patch git-push-with-tags
push-minor: bump-minor git-push-with-tags
push-major: bump-major git-push-with-tags

pypi-upload:
	python setup.py sdist bdist_wheel upload

release-patch: push-patch pypi-upload
release-minor: push-minor pypi-upload
release-major: push-major pypi-upload
