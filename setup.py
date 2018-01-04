from setuptools import setup

DEVELOPMENT_STATUS = "3 - Alpha"

setup(
    name='pylemon',
    version='0.0.5',
    description='An async and lightweight API framework for python .',
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
        'requests-toolbelt>=0.8.0',
    ],
    classifiers=[
        "Development Status :: %s" % DEVELOPMENT_STATUS,
        "Framework :: AsyncIO",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
