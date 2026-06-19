from setuptools import setup, find_packages

setup(
    name="ivycamlink",
    version="0.1.0",
    author="Logan Brown",
    author_init="lgnbrown@outlook.com",
    description="A lightweight ADB link bridge connecting headless Android cameras straight to OpenCV pipelines.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Swifts-32/IvyCamLink",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "opencv-python>=4.0.0",
        "numpy>=1.20.0",
    ],
)