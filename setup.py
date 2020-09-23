import os

from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md")) as f:
    readme = f.read()


packages = find_packages(exclude=["workspace"])

setup_args = {
    "name": "uectl",
    "version": "0.2.0",
    "description": "@uec_tlに使用するマルコフ連鎖による文章生成とテキスト処理のためのパッケージ",
    "long_description": readme,
    "long_description_content_type": "text/markdown",
    "license": "MIT License",
    "author": "Aki(@puman03)",
    "author_email": "a03ki04@gmail.com",
    "url": "https://github.com/A03ki/uec_tl_markov",
    "python_requires": ">=3.6, <3.9",
    "install_requires": ["emoji", "markovify", "neologdn", "pyyaml"],
    "extras_require": {
        "preprocessing": ["mecab-python3==0.996.5"],
        "tests": ["pytest"],
        "bot": ["tweepy"]
    },
    "packages": packages,
    "classifiers": [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Natural Language :: Japanese"
    ],
    "keywords": "uectl uec markov"
}

setup(**setup_args)
