import re
from setuptools import setup, find_packages

import sys
if sys.version_info < (3, 5):
    raise 'must use Python version 3.5 or higher'

with open('./gmailapi_backend/__init__.py', 'r') as f:
    MATCH_EXPR = "__version__[^'\"]+(['\"])([^'\"]+)"
    VERSION = re.search(MATCH_EXPR, f.read()).group(2).strip()


setup(
    name='django-gmailapi-backend',
    version=VERSION,
    packages=find_packages(),
    author="Michele Dolfi",
    author_email="michele.dolfi@gmail.com",
    license="Apache License 2.0",
    entry_points={
        'console_scripts': [
            'gmail_oauth2 = gmailapi_backend.bin.gmail_oauth2:main',
        ]
    },
    install_requires=[
        'google-api-python-client~=2.0.2',
        'google-auth~=1.28.0',
    ],
    url="https://github.com/dolfim/django-gmailapi-backend",
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    description='Email backend for Django which sends email via the Gmail API',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Topic :: Communications :: Email',
        'Development Status :: 4 - Beta'
    ],
)
