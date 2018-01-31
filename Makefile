init:
	pip install -r requirements.txt

release:
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
