from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in agri_dms/__init__.py
from agri_dms import __version__ as version

setup(
	name="agri_dms",
	version=version,
	description="Distributor Management System for Agriculture Machine Manufacturers",
	author="Agri-DMS Team",
	author_email="admin@agri-dms.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
