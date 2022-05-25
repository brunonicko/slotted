.PHONY: clean environment tests mypy format lint docs

clean:
	rm -rf ./docs/build .tox .mypy_cache .pytest_cache build dist slotted.egg-info
	find . -name '*.pyc' -delete
environment:
	python -m pip install --upgrade pip
	pip install -r requirements.txt --upgrade
	pip install -r dev_requirements.txt --upgrade
tests:
	python -m pytest tests_slotted.py
	python -m pytest README.rst --doctest-glob="*.rst"
mypy:
	mypy slotted.py
format:
	autoflake --remove-all-unused-imports --in-place slotted.py tests_slotted.py
	isort slotted.py tests_slotted.py ./docs/source/conf.py setup.py -m 3 -l 88 --up --tc --lbt 0 --color
	black slotted.py tests_slotted.py ./docs/source/conf.py setup.py
lint:
	flake8 slotted.py --count --ignore=F403,F401,W503,C901,E203 --max-complexity=10 --max-line-length=120 --statistics
	flake8 tests_slotted.py --count --ignore=F403,F401,W503,C901,E203 --max-complexity=10 --max-line-length=120 --statistics
docs:
	sphinx-build -M html ./docs/source ./docs/build
