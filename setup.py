import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="maida",
    version="0.1.2",
    author="lzc",
    author_email="624486877@qq.com",
    description="No description.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LZC6244/maida",
    packages=setuptools.find_packages(),
    install_requires=[
        'scrapy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
