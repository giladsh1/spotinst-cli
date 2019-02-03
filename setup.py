import setuptools
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='spotinstcli',
	version='0.1.3',
	description='CLI tool for interacting with Spotinst AWS elasticgroups',
	long_description=long_description,
	url='https://github.com/giladsh1/spotinst-cli',
	author='Gilad Sharaby',
	author_email='giladsh1@gmail.com',
	classifiers=[
		 'Programming Language :: Python :: 2',
         'Programming Language :: Python :: 2.7',
		 'License :: OSI Approved :: MIT License',
		 'Operating System :: OS Independent',
	 ],
	keywords='spotinst cli aws spotinst-cli',
	packages=find_packages(),
	entry_points={
		'console_scripts': [
			'spotinst-cli = spotinstcli:main',
		]
	},
	install_requires = [
		'prettytable',
		'requests',
		'PyInquirer',
		'clint',
		'wcwidth'
	],
	include_package_data=True
 )