# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

SHELL := /bin/bash
PYTHON = .venv/bin/python

PROJECT_NAME := <your project>
GITHUB_USER := <your user>
GITHUB_PROJECT := <your project>
PROJECT_DESCRIPTION := <your project description>

define LICENCE
MIT License

Copyright (c) 2021 Helena Oliveira e Júlio Felipe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
endef

export LICENCE

define PRE_COMMIT_CONFIG
repos:
    - repo: local
      hooks:
          - id: isort
            name: isort
            stages: [commit]
            language: system
            entry: isort src
            types: [python]

          - id: flake8
            name: flake8
            stages: [commit]
            language: system
            entry: flake8 src
            types: [python]
            exclude: setup.py

          - id: mypy
            name: mypy
            stages: [commit]
            language: system
            entry: mypy src
            types: [python]
            pass_filenames: false

          - id: pytest
            name: pytest
            stages: [commit]
            language: system
            entry: pytest tests -sv
            types: [python]
            pass_filenames: false

          - id: pytest-cov
            name: pytest
            stages: [push]
            language: system
            entry: pytest tests -sv -p no:warnings --cov=src --cov-fail-under=80
            types: [python]
            pass_filenames: false
endef

export PRE_COMMIT_CONFIG

define VSCODE_SETTINGS
{
    "python.pythonPath": "./venv/bin/python",
    "python.testing.unittestEnabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "-v",
        "-s",
        ".",
        "-p",
        "*test*.py"
    ],
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--max-line-length=120",
        "exclude=migrations,.venv"
    ],
    "editor.formatOnSave": true,
    "python.formatting.provider": "black",
    "files.exclude": {
        "/*.pyc": {
            "when": "$(basename).py"
        },
        "/pycache": true,
    },
}
endef

export VSCODE_SETTINGS

define SETUP_PY
import os

from src import __version__ as version

readme = os.path.join(os.path.dirname(__file__), "README.md")
long_description = open(readme).read()

SETUP_ARGS = dict(
    name="$(PROJECT_NAME)",
    version=version,
    description="$(PROJECT_DESCRIPTION)",
    long_description=long_description,
    url="https://github.com/$$(cat GITHUB_USER)/$(GITHUB_PROJECT)",
    author="<AUTHOR>",
    author_email="<EMAIL>",
    license="MIT",
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
    ],
    py_modules=[
        "src",
    ],
    install_requires=["sqlalchemy", "flask", "flask-cors"],
)

if __name__ == "__main__":
    from setuptools import find_packages, setup

    SETUP_ARGS["packages"] = find_packages()
    setup(**SETUP_ARGS)
endef

export SETUP_PY

# Commands

setup: init_project create_requirements_folder create_config_files install_requirements create_project_folders

init_project:
	@read -p "What is your project name?: " PROJECT_NAME; \
	echo "#" $$PROJECT_NAME > README.md;
	@read -p "What is your project description?: " #PROJECT_DESCRIPTION; \
	echo "$$LICENCE" > LICENCE;
	@read -p "What is your github username?: " ans && echo -n "$$ans" > GITHUB_USER; \
	printf '.mypy_cache\n.pytest_cache\n.venv\npycache\n.env' > .gitignore;
	@read -p "What is your github project name?: " GITHUB_PROJECT; \
	echo "$$SETUP_PY" > setup.py;
	# git init;

create_requirements_folder:
	mkdir requirements;
	printf '%s test.txt\n\nmypy\npytest\nisort\nflake8\nblack\npre-commit' '-r' > requirements/dev.txt;
	printf '%s prod.txt\n\ncoverage\npytest\npytest-cov\npytest-flask' '-r' > requirements/test.txt;
	printf 'Flask\nSQLAlchemy\nflask-cors' > requirements/prod.txt;
	printf '%s requirements/prod.txt' '-r' > requirements.txt;

create_config_files:
	printf '[mypy]\nignore_missing_imports = False\nmypy_path = ./src\ncheck_untyped_defs = True\n\n[mypy-pytest.*,sqlalchemy.*,redis.*]\nignore_missing_imports = True' > mypy.ini;
	printf '[flake8]\nignore = E722, W503\nmax-line-length = 120\nper-file-ignores =\n\t__init__.py: F401' > .flake8;
	printf '# http://editorconfig.org\n\nroot = true\n\n[*]\nindent_style = space\nindent_size = 4\ntrim_trailing_whitespace = true\ninsert_final_newline = true\ncharset = utf-8\nend_of_line = lf\n\n[*.bat]\nindent_style = tab\nend_of_line = crlf\n\n[LICENSE]\ninsert_final_newline = false\n\n[Makefile]\nindent_style = tab' > .editorconfig;
	@echo "$$PRE_COMMIT_CONFIG" > .pre-commit-config.yaml;
	mkdir .vscode
	@echo "$$VSCODE_SETTINGS" > .vscode/settings.json;
	mkdir tests
	touch tests/__init__.py
	printf '[pytest]\npython_files = *_test.py\naddopts = --tb=short\nfilterwarnings =\n\tignore::DeprecationWarning' > tests/pytest.ini
	mkdir src
	printf '__version__ = "0.3.0"' > src/__init__.py
    printf '[run]\nomit =\n\tmigrations/,\n\ttests/,\n\t.venv/,\n\t*/init.py\nbranch = True\n\n[coverage:report]\nskip_empty = true' > .coveragerc

create_project_folders:
	mkdir -p src/data/interfaces
	mkdir -p src/data/usecases
	touch src/data/interfaces/__init__.py
	touch src/data/usecases/__init__.py
	touch src/data/__init__.py
	mkdir -p src/domain/entities
	mkdir -p src/domain/usecases
	touch src/domain/entities/__init__.py
	touch src/domain/usecases/__init__.py
	touch src/domain/__init__.py
	mkdir -p src/infrastructure
	touch src/infrastructure/__init__.py
	mkdir -p src/presentation/controllers
	mkdir -p src/presentation/helpers
	mkdir -p src/presentation/errors
	touch src/presentation/controllers/__init__.py
	touch src/presentation/helpers/__init__.py
	touch src/presentation/errors/__init__.py
	touch src/presentation/__init__.py
	mkdir -p src/main/adapters
	mkdir -p src/main/composers
	mkdir -p src/main/configs
	mkdir -p src/main/interfaces
	mkdir -p src/main/routes
	touch src/main/adapters/__init__.py
	touch src/main/composers/__init__.py
	touch src/main/configs/__init__.py
	touch src/main/interfaces/__init__.py
	touch src/main/routes/__init__.py
	touch src/main/__init__.py

install_requirements:
	python -m venv .venv
	( \
       source .venv/bin/activate; \
       pip install -r requirements/dev.txt; \
	   pre-commit install; \
    )

unit-tests:
	${PYTHON} -m pytest -svv tests/unit --cov=src --cov-report=term-missing

black:
	${PYTHON} -m black -l 86 $$(find * -name '*.py')

create_db:
	$(CREATEDB)
