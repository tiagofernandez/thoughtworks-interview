default: develop

setup:
	pip install --upgrade virtualenv autoenv nose
	virtualenv -p python3 env

clean:
	find . -type f -name '*.pyc' -delete

test: clean develop
	nosetests -s

develop:
	python setup.py develop

install:
	python setup.py install

tar:
	python setup.py sdist
