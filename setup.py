from setuptools import setup

setup(
    name='pylemon',
    version='0.0.2',
    description='An async and lightweight restful framework for python .',
    url='https://github.com/joway/lemon',
    author='Joway Wang',
    author_email='joway.w@gmail.com',
    license='MIT',
    packages=['lemon'],
    keywords='lemon restful api async python',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
        'uvloop>=0.9.1',
        'httptools>=0.0.10',
        'requests>=2.18.4',
        'treelib>=1.5.1',
    ],
)
