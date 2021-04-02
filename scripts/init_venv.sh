#!/usr/bin/env bash

set -x
set -e

cd "$(dirname "$0")" || exit
cd ..

rm -r venv
python3 -m venv venv

source venv/bin/activate
which pip
which python

pip install -e git+https://github.com/robertradnai/vocabulary-lib@main#egg=vocabulary-RR
pip install -e .



pip freeze > requirements.txt
