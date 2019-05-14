import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="maida",
    version="0.0.10",
    author="lzc",
    author_email="624486877@qq.com",
    description="A small example package for me ( now is for sending email ).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LZC6244/maida",
    packages=setuptools.find_packages(),
    # install_requires=[
    #     'logging',
    # ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
