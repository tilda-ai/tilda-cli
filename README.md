
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
# clone the repo
git clone https://github.com/tilda/tilda.git
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

# install the tilda package on your machine
pipx install . --upgrade

tilda terminal "say hello"
```


## Usage

After installation, the tool can be run from the command line.

### Running the Terminal Agent

To run the terminal agent:


```shell
tilda terminal "Say Hello, World!"

# executed command
echo "Hello, World!"
```


To run the terminal agent with scoped execution context (in natural language):


```shell
terminal "rebuild packages with node v21" --scope "packages: types, common, shell-core"
```


## Contributing

Contributions to tilda are welcome and encouraged! 

Please feel free to clone the repository, make changes, and submit pull requests. You can also open issues if you find bugs or have feature requests.

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details.
