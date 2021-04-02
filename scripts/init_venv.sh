#!/usr/bin/env bash

set -x
set -e

cd "$(dirname "$0")" || exit
cd ..

rm -r venv
rm -r src
python3 -m venv venv

source venv/bin/activate
which pip
which python

pip install -e git+https://github.com/robertradnai/vocabulary-lib@main#egg=vocabulary-RR
pip install -e .


# vocabulary_srv will be installed from this project folder
# instead of from Github
pip freeze | grep -v "vocabulary_srv" > requirements.txt
