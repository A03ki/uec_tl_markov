from setuptools import find_packages, setup


packages = find_packages(exclude=["workspace"])

setup_args = {
    "name": "uectl",
    "version": "0.1.0",
    "description": "@uec_tlに使用するマルコフ連鎖による文章生成とテキスト処理のためのパッケージ",
    "license": "MIT License",
    "author": "Aki(@puman03)",
    "author_email": "a03ki04@gmail.com",
    "url": "https://github.com/A03ki/uec_tl_markov",
    "python_requires": "==3.6.*",
    "install_requires": ["emoji", "markovify", "neologdn", "pyyaml"],
    "extras_require": {
        "preprocessing": ["mecab-python3==0.996.5"],
        "tests": ["pytest"],
        "twitter": ["tweepy"]
    },
    "packages": packages
}

setup(**setup_args)
