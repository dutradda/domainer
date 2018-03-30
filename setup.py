#!/usr/bin/env python3

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import os.path
import sys


root_dir = os.path.dirname(os.path.abspath(__file__))
version_f = open(os.path.join(root_dir, 'domainer/version.py'))
install_requires = [
    'connexion-aiohttp>=1.5',
    'openapi21>=0.3.1'
]

if sys.version_info[0] > 2:
    install_requires.append('aiohttp==2.*')
    install_requires.append('aiohttp-jinja2==0.14.0')

tests_require = [
    'pytest',
    'pytest-cov',
    'mock'
]
setup_requires = [
    'pytest-runner',
    'flake8'
]
version = {}

exec(version_f.read(), version)
version = version['VERSION']

long_description = ''''''


class PyTest(TestCommand):

    user_options = [
        ('cov-html=', None, 'Generate html report'),
        ('filter=', None, "Pytest setence to filter (see pytest '-k' option)"),
        # ('vars=', None, 'Pytest external variables file')
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['--cov', 'domainer', '-xvv']
        self.cov_html = False
        self.filter = False
        # self.vars = 'pytest-vars.json'

        if sys.version_info[0] < 3:
            self.pytest_args.append('--cov-config=py2-coveragerc')
        else:
            self.pytest_args.append('--cov-config=py3-coveragerc')

    def finalize_options(self):
        TestCommand.finalize_options(self)
        # self.pytest_args.extend(['--variables', self.vars])

        if self.cov_html:
            self.pytest_args.extend(['--cov-report', 'html'])
        else:
            self.pytest_args.extend(['--cov-report', 'term-missing'])

        if self.filter:
            self.pytest_args.extend(['-k', self.filter])

        self.pytest_args.extend(['tests'])

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='domainer',
    packages=find_packages(),
    include_package_data=True,
    version=version,
    description='A simple and intuitive Domain Driven Design (DDD) '
                'framework for Python, with CRUD operations for SQL '
                'and NoSQL databases.',
    long_description=long_description,
    author='Diogo Dutra',
    author_email='dutradda@gmail.com',
    url='https://github.com/dutradda/domainer',
    keywords='ddd domain-driven-design design-patterns software-architecture '
             'openapi oai swagger rest api crud api-first orm sqlalchemy '
             'redis elasticsearch',
    license='MIT',
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    test_suite='tests',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Topic :: Text Processing',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={
        'console_scripts': [
            'domainer = domainer.cli:main'
        ]
    }
)
