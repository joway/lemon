init:
    pip install -r requirements.txt

release:
    python setup.py sdist upload

test:
    python setup.py test

lint:
    pycodestyle --exclude docs/

docs:
    sphinx-build -b html docs/source docs/build
