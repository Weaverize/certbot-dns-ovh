import sys

from distutils.core import setup
from setuptools import find_packages

version = '0.1.0.dev0'

# Remember to update local-oldest-requirements.txt when changing the minimum
# acme/certbot version.
install_requires = [
	'acme>=0.21.1',
    'certbot>=0.21.1',
    'setuptools',
	'ovh'
]

setup(
    name='certbot-dns-ovh',
    version=version,
    description="OVH DNS Authenticator plugin for Certbot",
    url='https://github.com/weaverize/certbot-dns-ovh',
    author="Weaverize",
    author_email='dev@weaverize.com',
    license='MIT',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    keywords=['certbot', 'ovh'],
    entry_points={
        'certbot.plugins': [
            'dns-ovh = certbot_dns_ovh.dns_ovh:Authenticator',
        ],
    }
)