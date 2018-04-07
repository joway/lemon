init:
	pip install -r requirements.txt

release:
	git tag `cat setup.py | grep 'PACKAGE_VERSION = ' | sed "s/PACKAGE_VERSION = //"`
	python setup.py sdist upload

test:
	pytest -qq

lint:
	pycodestyle --exclude docs/ --ignore E501

hint:
	mypy lemon --ignore-missing-imports

check:
	make hint lint test

docs:
	sphinx-build -b html docs/source docs/build
