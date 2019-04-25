from setuptools import setup

PACKAGE_VERSION = '0.4.0'
PACKAGE_REQUIRES = [
    'uvicorn==0.7.0',
    'kua==0.2',
    'werkzeug==0.15.2',
]
DEVELOPMENT_STATUS = '5 - Production/Stable'

setup(
    name='pylemon',
    version=PACKAGE_VERSION,
    description='An async and lightweight API framework for python .',
    url='https://github.com/joway/lemon',
    author='Joway Wang',
    author_email='joway.w@gmail.com',
    license='MIT',
    packages=['lemon'],
    keywords='lemon restful api async python',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=PACKAGE_REQUIRES,
    classifiers=[
        'Development Status :: %s' % DEVELOPMENT_STATUS,
        'Framework :: AsyncIO',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
