init:
    pip install -r requirements.txt

release:
    python setup.py sdist upload

test:
    python setup.py test

docs:
    sphinx-build -b html docs/source docs/build
