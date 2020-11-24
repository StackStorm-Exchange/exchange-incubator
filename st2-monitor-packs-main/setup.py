from setuptools import setup, find_packages

requirements = ["ipython>=6", "nbformat>=4", "nbconvert>=5", "requests>=2"]
setup(
    name="maximo-pkg",  # Replace with your own username
    version="0.0.1",
    author="Vaibhav Goel",
    author_email='vagoel66@in.ibm.com',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.2',
)
