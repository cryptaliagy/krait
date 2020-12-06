pip install -r requirements.txt -r test-requirements.txt -e .;
pre-commit install;
pre-commit run --all-files;
mypy;
pytest;
