import os
import setuptools  # type: ignore


with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = [line.strip(os.linesep) for line in fh.readlines()]


setuptools.setup(
    name="slotted",
    version="3.1.1",
    author="Bruno Nicko",
    author_email="brunonicko@gmail.com",
    description="Collection of lower-level utilities that enhance code compatibility and validation.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/brunonicko/slotted",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    package_data={"slotted": ["py.typed"]},
    install_requires=install_requires,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires=">= 2.7, != 3.0.*, != 3.1.*, != 3.2.*, != 3.3.*, != 3.4.*, != 3.5.*, != 3.6.*",
    tests_require=["pytest"],
)
