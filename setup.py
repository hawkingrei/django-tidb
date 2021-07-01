import io
import os

from setuptools import find_packages, setup

BASE_DIR = os.path.dirname(__file__)
VERSION_FILENAME = os.path.join(BASE_DIR, "version.py")
PACKAGE_INFO = {}
with open(VERSION_FILENAME) as f:
    exec(f.read(), PACKAGE_INFO)
version = PACKAGE_INFO["__version__"]

setup(
    name='django-tidb',
    dependencies=["sqlparse >= 0.3.0", "mysqlclient >= 1.4.0"],
    version=version,
    python_requires='>=3.6',
    url='https://github.com/pingcap/django-tidb',
    maintainer='Weizhen Wang',
    maintainer_email='wangweizhen@pingcap.com',
    description='Django backend for tidb',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    project_urls={
        'Source': 'https://github.com/pingcap/django-tidb',
        'Tracker': 'https://github.com/pingcap/django-tidb/issues',
    },
)
