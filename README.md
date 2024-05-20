
# ~tilda

A command-line interface based on AI for automating software development, from single actions and steps to complete processes.

## Features

- **Terminal Agent**: Gets that terminal command you were looking for.

## Installation

To install the CLI, you need Python >=3.12 installed on your system.

For now, to run tilda locally from your command line, you can install it directly from source by cloning the repository.

1. Install [uv](https://github.com/astral-sh/uv) or use pip3.

2. Install [pipx](https://github.com/pypa/pipx) for the global installation of ~tilda on your machine.


```shell
# ---
# Installation
# ---

#install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

#install pipx
brew install pipx
pipx ensurepath

# clone the repo
git clone git@github.com:tilda-ai/tilda-cli.git
cd tilda

# create virtual env
uv venv 
source .venv/bin/activate

# install dependencies
uv pip install -r requirements.txt

# build the package from source
python3 -m build

# deactivate venv (or run the next command in a new terminal)
deactivate

# install the tilda package globally
pipx install .
# (to delete the global installation)
pipx uninstall tilda

tilda terminal "clean all python cache files in src"

# ---
# Development
# ---

# 1. install the tilda package in edit mode
pipx install -e .

# 2. run watch mode
python3 watch.py
```


## Usage

After installation, the tool can be run from the command line.

### Running the Terminal Agent

To run the terminal agent:


```shell
tilda terminal "say Hello, World!"

# executed command
echo "Hello, World!"
```


To run the terminal agent with a mocked response during development:


```shell
tilda terminal "" --mock
```


## Contributing

Contributions to tilda are welcome and encouraged! 

Please feel free to clone the repository, make changes, and submit pull requests. You can also open issues if you find bugs or have feature requests.

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details.
