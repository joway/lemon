init:
	pip install -r requirements.txt

release:
	python setup.py sdist upload

test:
	python setup.py test

lint:
	pycodestyle --exclude docs/ --ignore E501

hint:
	mypy lemon --ignore-missing-imports

check:
	make hint test lint

docs:
	sphinx-build -b html docs/source docs/build
