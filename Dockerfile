FROM python:3.6

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y mecab \
    && apt-get install -y mecab-ipadic \
    && apt-get install -y libmecab-dev \
    && apt-get install -y mecab-ipadic-utf8 \
    && apt-get install -y swig \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --upgrade pip \
    && pip install --progress-bar off -U setuptools

WORKDIR /home/uec_tl_markov

COPY ./uectl ./uectl
COPY ./setup.py ./README.md ./

RUN pip install --progress-bar off ".[preprocessing, tests]"
