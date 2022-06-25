from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in lonius_payments/__init__.py
from lonius_payments import __version__ as version

setup(
	name="lonius_payments",
	version=version,
	description="App for managing client payments",
	author="Lonius Devs",
	author_email="info@lonius.co.ke",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
