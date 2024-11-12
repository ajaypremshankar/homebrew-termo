from setuptools import setup

setup(
    name="macro-cli",
    version="1.0.1",
    description="A CLI tool for recording and running macros in the terminal.",
    author="Ajay Prem Shankar",
    author_email="ajaypremshankar@gmail.com",
    py_modules=["macro"],
    install_requires=[
        "click",
        "setuptools"
    ],
    entry_points={
        "console_scripts": [
            "mrec=macro:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
