.PHONY: test

all:
	# Available options: test, coverage, install, install_dev

test:
	pytest -vv --ignore='ark/anki' --rootdir=test

coverage:
	pytest -vv --ignore='ark/anki' --rootdir=test --cov=ark --cov-report html

install:
	pip3 install -e '.'

install_dev:
	pip3 install -e '.[dev]'
