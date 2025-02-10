# UV

## Usage
```
## install uv on OS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a venv for an existing project
uv venv --python 3.12

# Using your venv
uv venv

## create new project (Monorepo - Another project in the main project)
uv init myproj

## create new project (Standalone Project)
uv init myproj --no-workspace

## install packages
uv add django requests "pandas>=2.3"

## Installing Dev Packages
uv add <dependency> --group dev

## remove package
uv remove django

## see pkg dependency tree
uv tree

## run a python script directly w/o starting venv
uv run main.py

## install specific version of python
uv python list
uv python install 3.12

## start a new project and pin it to Python 3.12
uv init myproject
uv python pin 3.12
uv add django
uv run main.py (will automatically install py3.12 and django into venv)

## UV / UVX

uv tool install ruff
uv tool uninstall ruff
uv tool upgrade ruff
uv tool dir
uv tool update-shell

uv run tool ruff check (or uvx ruff)
uvx ruff check

## update uv version to latest
uv self update
```
