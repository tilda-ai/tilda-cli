
# ~tilda

A command-line interface based on AI for automating software development, from single actions and steps to complete processes.

## Features

- **Terminal Command**: Get that terminal command you were looking for.

## Installation

To use the `tilda CLI, you need Python installed on your system.

The tool has been tested with Python 3.12.2.

For now you can install it directly from source by cloning the repository.

1. Install uv or use pip3 [astral/uv](https://github.com/astral-sh/uv)

2. Install pipx for the global installation of ~tilda on your machine [pypa/pipx](https://github.com/pypa/pipx)


```shell
git clone https://github.com/tilda/tilda.git
cd tilda
uv venv 
source .venv/bin/activate

# build the package from source
python3 setup.py sdist bdist_wheel

# exit venv
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
```

To run the terminal command with permissive execution settings:

```shell
terminal --careless "rm -rf /example"
```

**Warning:** Use the `--careless` flag with caution, especially when performing operations that can modify or delete data.

## Contributing

Contributions to ~tilda are welcome and encouraged! Please feel free to clone the repository, make changes, and submit pull requests. You can also open issues if you find bugs or have feature requests.

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details.
