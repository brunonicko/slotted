import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slotted-brunonicko",
    version="0.0.1",
    author="Bruno Nicko",
    author_email="brunonicko@gmail.com",
    description="Enforces usage of '__slots__' for python classes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brunonicko/slotted",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
