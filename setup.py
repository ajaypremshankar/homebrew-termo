from setuptools import setup, find_packages

setup(
    name="Termo",
    version="1.1.1",
    description="A CLI tool for recording and running macros in the terminal.",
    author="Ajay Prem Shankar",
    author_email="ajaypremshankar@gmail.com",
    packages=find_packages(include=["app", "app.*"]),
    py_modules=["termo"],
      # Include the `commands` package
    install_requires=[
        "click",
        "setuptools",
        "paramiko"
    ],
    entry_points={
        "console_scripts": [
            "tm=termo:cli",
            "termo=termo:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
