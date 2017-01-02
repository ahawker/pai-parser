# pai-parser

[![Build Status](https://travis-ci.org/ahawker/pai-parser.svg?branch=master)](https://travis-ci.org/ahawker/pai-parser)
[![Coverage Status](https://coveralls.io/repos/github/ahawker/pai-parser/badge.svg?branch=master)](https://coveralls.io/github/ahawker/pai-parser?branch=master)

Describe and parse shell-safe strings into a structured syntax.

This package is used as the underlying parser for [pai-lang](https://github.com/ahawker/pai-lang).

### Status

`pai-parser` is in alpha stage and not yet used by any production workloads.

### Installation

Install latest production build using [pip](https://pypi.python.org/pypi/pip):
```bash
    $ pip install pai_parser
```

Install latest development build using [pip](https://pypi.python.org/pypi/pip):
```bash
    $ pip install -i https://testpypi.python.org/pypi pai_parser
```

Install from source code:
```bash
    $ git clone git@github.com:ahawker/pai_parser.git
    $ cd pai_parser
    $ python setup.py install
```

### Deployment

Package deployments to index servers are automatically performed by [Travis CI](https://travis-ci.org/).

[PyPI](https://pypi.python.org/pypi/pai-parser) - Hosts **Official** Builds
[TestPyPI](https://testpypi.python.org/pypi/pai-parser) - Hosts **Development** Builds

Tagged versions of the `master` branch will be deployed to the official PyPI index server while non-tagged versions will be deployed
to the test PyPI index server.

To kick off a new, official deployment, just run one of the following:

**Patch** Version Release: Use this when you make backwards-compatible bug fixes.
```bash
    $ make push-patch
```

**Minor** Version Release: Use this when you add functionality in a backwards-compatible manner.
```bash
    $ make push-minor
```

**Major** Version Release: Use this when you make incompatible API changes.
```bash
    $ make push-major
```

### License

[Apache 2.0](LICENSE)
