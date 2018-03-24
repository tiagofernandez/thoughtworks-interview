default: develop

setup:
	pip install --upgrade virtualenv autoenv
	virtualenv -p python3 env

deps:
	pip install -r requirements.txt --quiet

clean:
	find . -type f -name '*.pyc' -delete

test: clean
	nosetests -s

develop: deps
	python setup.py develop

install:
	python setup.py install

tar:
	python setup.py sdist

run:
	./trains/app.py $(input)
