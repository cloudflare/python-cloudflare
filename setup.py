#!/usr/bin/env python
"""Cloudflare API code - setup.py file"""

from setuptools import setup, find_packages
from CloudFlare import __version__


def main():
    """Cloudflare API code - setup.py file"""

    with open('README.rst') as read_me:
        long_description = read_me.read()

    setup(
        name='cloudflare',
        version=__version__,
        description='Python wrapper for the Cloudflare v4 API',
        long_description=long_description,
        author='Martin J. Levy',
        author_email='martin@cloudflare.com',
        # maintainer='Martin J. Levy',
        # maintainer_email='martin@cloudflare.com',
        url='https://github.com/cloudflare/python-cloudflare',
        license='MIT',
        packages=['cli4', 'examples'] + find_packages(),
        include_package_data=True,
        install_requires=['requests', 'logger', 'future', 'pyyaml'],
        keywords='cloudflare',
        entry_points={
            'console_scripts': [
                'cli4=cli4.__main__:main'
            ]
        },
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6'
        ]
    )


if __name__ == '__main__':
    main()
