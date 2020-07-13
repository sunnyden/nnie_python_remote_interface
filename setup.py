import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nnie",
    version="0.1",
    author="Haoqing Deng",
    license='MIT',
    author_email="dhq.sunny@gmail.com",
    description="NNIE Python Interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
    'opencv-python',
    'numpy',
    ],
    url="https://github.com/sunnyden/nnie_python_remote_interface",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
