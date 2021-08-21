default: live_test

venv:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade setuptools && pip install -r requirements.txt && pip install -e .

live_test: venv
	. venv/bin/activate && pip -V && which python && python scripts/live_test.py

clean:
	rm -rf venv
	find . -type f -name '*.pyc' -delete

test: venv
	. venv/bin/activate && pip install flake8 pytest
	# stop the build if there are Python syntax errors or undefined names
	. venv/bin/activate && cd vocabulary_srv && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	. venv/bin/activate && cd vocabulary_srv && flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statis
	. venv/bin/activate && pytest tests

build:
	sudo docker build -t vocabulary_srv -f Dockerfile .

.PHONY: all run clean test