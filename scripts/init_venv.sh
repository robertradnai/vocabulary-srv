cd $'dirname('$0')' || exit
cd ..

rm -r venv
python3 -m venv venv
pip install -e .
pip install ../../packages/Vocabulary/vocabulary_RR-0.1-py3-none-any.whl