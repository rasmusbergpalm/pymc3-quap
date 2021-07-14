import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pymc3-quap',
    version='1.0.1',
    author="Rasmus Berg Palm",
    author_email="rasmusbergpalm@gmail.com",
    description="Quadratic approximation for PyMC3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rasmusbergpalm/pymc3-quap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
