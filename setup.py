import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slotted",
    version="1.2.1",
    author="Bruno Nicko",
    author_email="brunonicko@gmail.com",
    description="Enforces usage of '__slots__' for python classes",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/brunonicko/slotted",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    package_data={"slotted": ["__init__.pyi", "py.typed"]},
    install_requires=["six", "typing; python_version < '3.5'"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires=">=2.7",
    tests_require=["pytest"],
)
