import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BlindSailor",
    version="0.1.0",
    author="",
    author_email="",
    description="",
    long_description=long_description,
    license="GPLv3+",
    url="https://github.com/ADX-S17/BlindSailor.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developpers",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Mostly Unix",
    ],
)
